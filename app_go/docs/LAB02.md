# Build strategy
Docker builds image in two stages:
- First stage builds application from
source go code under SDK image.
- Second stage runs application
executable under distroless static image.

# Size comparison
Image built without multi-staging
under go SDK image has size of 947MB,
whereas image with multi-staging has
size of 10.5MB which makes difference
of almost 100 times of space.

# Multi-stage builds importance
Using multi-stage container builds
for compiled languages allows numeral
save in image size, because compiler itself
takes much space, but is not needed
for running the application itself,
since runtime is embedded to executable.
Therefore removing space-consuming
compiler from final image reduces
image size significantly.

# Terminal outputs
Images info:
```
REPOSITORY           TAG            IMAGE ID       CREATED          SIZE
infoservice          go-dev         cfa7da73fc3f   40 minutes ago   10.5MB
infoservice          go-bad         460c3cec266e   45 minutes ago   947MB
```

Building image:
```
[+] Building 6.7s (13/13) FINISHED                                                                                                                                               docker:default
 => [internal] load build definition from Dockerfile                                                                                                                                       0.0s
 => => transferring dockerfile: 234B                                                                                                                                                       0.0s
 => [internal] load metadata for gcr.io/distroless/static-debian12:latest                                                                                                                  0.5s
 => [internal] load metadata for docker.io/library/golang:1.25                                                                                                                             1.6s
 => [auth] library/golang:pull token for registry-1.docker.io                                                                                                                              0.0s
 => [internal] load .dockerignore                                                                                                                                                          0.0s
 => => transferring context: 189B                                                                                                                                                          0.0s
 => [builder 1/4] FROM docker.io/library/golang:1.25@sha256:ce63a16e0f7063787ebb4eb28e72d477b00b4726f79874b3205a965ffd797ab2                                                               0.0s
 => [stage-1 1/2] FROM gcr.io/distroless/static-debian12:latest@sha256:cd64bec9cec257044ce3a8dd3620cf83b387920100332f2b041f19c4d2febf93                                                    0.0s
 => [internal] load build context                                                                                                                                                          0.0s
 => => transferring context: 8.52MB                                                                                                                                                        0.0s
 => CACHED [builder 2/4] WORKDIR /app                                                                                                                                                      0.0s
 => [builder 3/4] COPY . .                                                                                                                                                                 0.0s
 => [builder 4/4] RUN CGO_ENABLED=0 go build -o app                                                                                                                                        5.0s
 => CACHED [stage-1 2/2] COPY --from=builder /app/app /                                                                                                                                    0.0s
 => exporting to image                                                                                                                                                                     0.0s
 => => exporting layers                                                                                                                                                                    0.0s
 => => writing image sha256:cfa7da73fc3fd694f3a5473a882ae4eaf2b22a38276f268096d60194c2b903d0                                                                                               0.0s
 => => naming to docker.io/library/infoservice:go-dev
```

# Technical explanation of each stage's purpose
- First stage is needed to build application executable
- Second stage's purpose is to run application
