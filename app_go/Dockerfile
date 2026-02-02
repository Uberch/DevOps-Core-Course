# Building stage
from golang:1.25 as builder
workdir /app
copy . .
run CGO_ENABLED=0 go build -o app

# Runtime
from gcr.io/distroless/static-debian12
copy --from=builder /app/app /
cmd ["/app"]
