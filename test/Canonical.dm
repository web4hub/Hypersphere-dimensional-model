dm 0.1

model Hypersphere {

    dimension 4

    axes [x,y,z,w]

    geometry {
        equation:
            x² + y² + z² + w² <= R²
    }

    topology {
        manifold: S3
        boundary: none
    }

    observation {
        target: 3D
        method: slice
        axis: w
        range: [-R,R]
    }

    projection {
        method: perspective
    }

    animation {
        parameter: w
        steps: 120
    }

    render {
        mode: volume
        interactive: true
    }
}
