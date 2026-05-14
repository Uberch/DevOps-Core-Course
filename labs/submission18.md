# Task 1
## Installation steps
Pre-installed on my nixos system

## `default.nix`
```nix
{ pkgs ? import <nixpkgs> {} }: # Inputs
pkgs.python3Packages.buildPythonApplication {
	pname = "devops-info-service"; # Package name
	version = "1.0.0"; # Version
	src = ./.; # Source dir

	format = "other";

	propagatedBuildInputs = with pkgs.python3Packages; [ # Packages, requiered for build (and propagated to dependencies)
		fastapi
		uvicorn
	];

	nativeBuildInputs = [ pkgs.makeWrapper ]; # Packages, requiered for build

    # Installation script
	installPhase = ''
		mkdir -p $out/bin
		cp src/app.py $out/bin/devops-info-service
		chmod +x $out/bin/devops-info-service

		# Wrap with Python interpreter so it can execute
		wrapProgram $out/bin/devops-info-service \
			--prefix PYTHONPATH : "$PYTHONPATH"
	'';
}
```

## Store path
`/nix/store/y1j4wjhl1v1518chqbrjwksa9mrrbzzv-devops-info-service-1.0.0`
Store path identical by construction

## `pip install` vs Nix derivation
| Aspect | `pip install` | Nix |
|--------|-------------------|--------------|
| Python version | System-dependent | Pinned in derivation |
| Dependency resolution | Runtime (`pip install`) | Build-time (pure) |
| Reproducibility | Approximate (with lockfiles) | Bit-for-bit identical |
| Portability | Requires same OS + Python | Works anywhere Nix runs |
| Binary cache | No | Yes (cache.nixos.org) |
| Isolation | Virtual environment | Sandboxed build |
| Store path | N/A | Content-addressable hash |

## `requirements.txt`
`requirements.txt` provide weaker guarantees than Nixos, because Nix guarantees bit-by-bit identical builds, and requirements give aproximate locks for dependency versions

## Screenshots
![App running from nix-built version](./lab18/lab1running.png)

## Nix store paths
Paths in nix store have type of `/nix/store/<derivation hash>-<package name>-<version>`

## Reflection
Nix would remove any problems with dependencies

# Task 2
## `docker.nix`
```nix
{ pkgs ? import <nixpkgs> {} }:

let
  app = import ./default.nix { inherit pkgs; };
in
pkgs.dockerTools.buildLayeredImage {
  name = "devops-info-service-nix"; # Container name
  tag = "1.0.0"; # Container tag

  contents = [ app ]; # Contents of containter

  config = { # Configuration of container
    Cmd = [ "${app}/bin/devops-info-service" ];
    ExposedPorts = {
      "5000/tcp" = {};
    };
  };

  created = "1970-01-01T00:00:01Z";  # Reproducible timestamp
}
```

## Docker file vs Nix
| Aspect | Lab 2 Traditional Dockerfile | Lab 18 Nix dockerTools |
|--------|------------------------------|------------------------|
| **Base images** | `python:3.13-slim` (changes over time) | No base image (pure derivations) |
| **Timestamps** | Different on each build | Fixed or deterministic |
| **Package installation** | `pip install` at build time | Nix store paths (immutable) |
| **Reproducibility** | ❌ Same Dockerfile → Different images | ✅ Same docker.nix → Identical images |
| **Caching** | Layer-based (breaks on timestamp) | Content-addressable (perfect caching) |
| **Image size** | ~150MB+ with full base image | ~50-80MB with minimal closure |
| **Portability** | Requires Docker | Requires Nix (then loads to Docker) |
| **Security** | Base image vulnerabilities | Minimal dependencies, easier auditing |
| **Lab 2 Learning** | Best practices, non-root user | Build on Lab 2 knowledge |

## Hash
```bash
/nix/store/ipw3p4rvgnzhq5a4ll5ggfb9z23nnwws-devops-info-service-nix.tar.gz
c188963bccc9751b22dc882329722f42a372e48fea8cbbf23fd65ae94fe6e313  result
/nix/store/ipw3p4rvgnzhq5a4ll5ggfb9z23nnwws-devops-info-service-nix.tar.gz
c188963bccc9751b22dc882329722f42a372e48fea8cbbf23fd65ae94fe6e313  result
```
Hashes are same by construction

## `docker history`
```bash
IMAGE          CREATED   CREATED BY   SIZE      COMMENT
441122499869   N/A                    300B      store paths: ['/nix/store/jdgi0aiv8403z3ix8ygxbfh61rzb21rl-devops-info-service-nix-customisation-layer']
<missing>      N/A                    12.6kB    store paths: ['/nix/store/63cfdhali36l7lm1zlp2q1yzmqlvpf2y-devops-info-service-1.0.0']
<missing>      N/A                    1.58MB    store paths: ['/nix/store/q1xbcz78q7qp51pwxvd7yl593y74v0xh-python3.13-fastapi-0.116.1']
<missing>      N/A                    5.44MB    store paths: ['/nix/store/10h9alp34gf83f00v1j0irab82n4zavg-python3.13-pydantic-2.11.7']
<missing>      N/A                    5.51MB    store paths: ['/nix/store/xi3gl6v4b3gw28lig89gbkzkn50fd1nj-python3.13-pydantic-core-2.33.2']
<missing>      N/A                    960kB     store paths: ['/nix/store/qp1p9y50adz6mgas3b45vnkhi46dfi7b-python3.13-starlette-0.47.2']
<missing>      N/A                    1.69MB    store paths: ['/nix/store/nxb9m8bpm10197r0c504y73m3r19zgrz-python3.13-anyio-4.11.0']
<missing>      N/A                    802kB     store paths: ['/nix/store/jjh9yygprkifwharwf0g5qr55mwyvkc5-python3.13-uvicorn-0.35.0']
<missing>      N/A                    1.23MB    store paths: ['/nix/store/in716x64gf5c99llz3abnsm71kiqcj2q-python3.13-click-8.2.1']
<missing>      N/A                    934kB     store paths: ['/nix/store/b8xwwa4ap3nrfg4mxpkq7vnnxxsdwybk-python3.13-idna-3.11']
<missing>      N/A                    125kB     store paths: ['/nix/store/x9xhq47r11hpcp6sdm69v2200g7vd747-python3.13-typing-inspection-0.4.2']
<missing>      N/A                    504kB     store paths: ['/nix/store/qfbq9xq5cy2i3z8fmi0kxghw7if9k8kw-python3.13-typing-extensions-4.15.0']
<missing>      N/A                    267kB     store paths: ['/nix/store/vws161bf1plrax5xwi2bac7d50vlsh7p-python3.13-h11-0.16.0']
<missing>      N/A                    102kB     store paths: ['/nix/store/0khqpcnj44bbg0mlhnz47kah31q2j0iz-python3.13-annotated-types-0.7.0']
<missing>      N/A                    38.8kB    store paths: ['/nix/store/c2ghbbyahc0qy6bfz2cb87c39givlici-python3.13-sniffio-1.3.1']
<missing>      N/A                    111MB     store paths: ['/nix/store/cdaifv92znxy5ai4sawricjl0p5b9sgf-python3-3.13.11']
<missing>      N/A                    9.97MB    store paths: ['/nix/store/gnpwfj9gpk8ll7dhf65a6r5gjbs4qbap-gcc-14.3.0-lib']
<missing>      N/A                    9.27MB    store paths: ['/nix/store/2p91cylbmdv4si5j818pnsg6qcbgin72-openssl-3.6.0']
<missing>      N/A                    509kB     store paths: ['/nix/store/gwyr8gxfj0rm2hnvx47zlfy5xvlwsd05-readline-8.3p1']
<missing>      N/A                    3.95MB    store paths: ['/nix/store/8bh8g107igzm703ib6vhslnagm1j47km-sqlite-3.50.4']
<missing>      N/A                    3.24MB    store paths: ['/nix/store/kpi3v5fl8hlgy5lagjvn6ayq78mla49k-ncurses-6.5']
<missing>      N/A                    2.01MB    store paths: ['/nix/store/hdy5qs834h84dhb85hxjss6mgqjjbx11-util-linux-minimal-2.41.3-lib']
<missing>      N/A                    1.84MB    store paths: ['/nix/store/j8645yndikbrvn292zgvyv64xrrmwdcb-bash-5.3p3']
<missing>      N/A                    843kB     store paths: ['/nix/store/hd4ff821999qr8iazn8fb42y0zzaarfp-xz-5.8.1']
<missing>      N/A                    449kB     store paths: ['/nix/store/znzrrwird7n8vkapi0rp4acv27j3ky01-gdbm-1.26-lib']
<missing>      N/A                    301kB     store paths: ['/nix/store/8hsj833zsm1bxhg49kykya3gn6gpp8jg-expat-2.7.3']
<missing>      N/A                    224kB     store paths: ['/nix/store/cwnb9q1xpw5rzss11pwjlz65jpl6m41d-mpdecimal-4.0.1']
<missing>      N/A                    131kB     store paths: ['/nix/store/nymigg679qmp97i3gilldx27p3ylfqy9-zlib-1.3.1']
<missing>      N/A                    83.6kB    store paths: ['/nix/store/f0rzmqp8qmlrpsnm1jp6hgh4f7030fsa-bzip2-1.0.8']
<missing>      N/A                    72.5kB    store paths: ['/nix/store/c86nvwib4x4w4lkd3qw2aw40a354b6yd-libffi-3.5.2']
<missing>      N/A                    30MB      store paths: ['/nix/store/wqfs0wh0wp6vdcbbck3wzk5v15qy17m7-glibc-2.40-66']
<missing>      N/A                    353kB     store paths: ['/nix/store/hxcmad417fd8ql9ylx96xpak7da06yiv-libidn2-2.3.8']
<missing>      N/A                    1.9MB     store paths: ['/nix/store/xh1ff9c9c0yv1wxrwa5gnfp092yagh7v-tzdata-2025b']
<missing>      N/A                    2.08MB    store paths: ['/nix/store/3rkccxj7vi0p2a0d48c4a4z2vv2cni88-libunistring-1.4.1']
<missing>      N/A                    201kB     store paths: ['/nix/store/2a3izq4hffdd9r9gb2w6q2ibdc86kss6-xgcc-14.3.0-libgcc']
<missing>      N/A                    201kB     store paths: ['/nix/store/n600a20z97mhhdnry40lp47nmnv16py5-gcc-14.3.0-libgcc']
<missing>      N/A                    118kB     store paths: ['/nix/store/m3954qff15v7z1l6lpyqf8v2h47c7hv2-mailcap-2.1.54']
```

## Analysis
Because timestamps also hashed in traditional Docker

## Reflection
I wouldn`t write Dockerfile

## Practical scenarios
- CI/CD
- security audits
- rollbacks
