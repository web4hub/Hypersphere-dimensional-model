module SpaceCapture (
    input  logic        clk,
    input  logic        reset,

    // Sensor/estimator inputs
    input  logic        target_detected,
    input  logic        target_identified,
    input  logic        tracking_valid,

    // Relative distance, millimeters
    input  logic [31:0] relative_distance,

    // Relative velocity, millimeters/second
    input  logic [31:0] relative_velocity,

    // Actuator outputs
    output logic        approach_enable,
    output logic        capture_enable,

    // Mission status
    output logic [2:0]  mission_state
);

    typedef enum logic [2:0] {
        SEARCH  = 3'd0,
        IDENTIFY = 3'd1,
        TRACK   = 3'd2,
        APPROACH = 3'd3,
        CAPTURE = 3'd4,
        VERIFY  = 3'd5
    } state_t;

    state_t state, next_state;

    // Prototype safety thresholds
    localparam logic [31:0] SAFETY_RADIUS_MM = 32'd5000;
    localparam logic [31:0] CAPTURE_RADIUS_MM = 32'd1000;
    localparam logic [31:0] MAX_CAPTURE_SPEED = 32'd100;

    always_comb begin

        next_state = state;

        case (state)

            SEARCH: begin
                if (target_detected)
                    next_state = IDENTIFY;
            end

            IDENTIFY: begin
                if (target_identified)
                    next_state = TRACK;
            end

            TRACK: begin
                if (tracking_valid)
                    next_state = APPROACH;
            end

            APPROACH: begin

                if (relative_distance <= CAPTURE_RADIUS_MM &&
                    relative_velocity <= MAX_CAPTURE_SPEED)
                    next_state = CAPTURE;
            end

            CAPTURE: begin
                next_state = VERIFY;
            end

            VERIFY: begin
                next_state = VERIFY;
            end

            default:
                next_state = SEARCH;

        endcase
    end


    always_ff @(posedge clk) begin

        if (reset) begin
            state <= SEARCH;
        end
        else begin
            state <= next_state;
        end

    end


    always_comb begin

        approach_enable = 1'b0;
        capture_enable  = 1'b0;

        case (state)

            APPROACH:
                approach_enable = 1'b1;

            CAPTURE:
                capture_enable = 1'b1;

            default: begin
                approach_enable = 1'b0;
                capture_enable  = 1'b0;
            end

        endcase

    end


    assign mission_state = state;

endmodule
