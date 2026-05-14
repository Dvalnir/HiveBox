# https://mcr.microsoft.com/en-us/artifact/mar/devcontainers/base/tag/noble
# https://github.com/devcontainers/images/tree/main/src/base-ubuntu
FROM mcr.microsoft.com/devcontainers/base:noble
USER vscode
RUN mkdir -p ~/.local/bin
# UV
RUN curl -LsSf "https://astral.sh/uv/install.sh" | sh
# TASKFILE
RUN sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b ~/.local/bin
# HADOLINT
RUN curl --location "https://github.com/hadolint/hadolint/releases/download/v2.14.0/hadolint-linux-x86_64" \
-o hadolint \
--output-dir ~/.local/bin/ \
&& \
chmod u+x ~/.local/bin/hadolint
# KUBECTL
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
-o kubectl \
--output-dir ~/.local/bin/ \
&& \
chmod u+x ~/.local/bin/kubectl
# HELM
RUN curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-4 | PATH="$HOME/.local/bin:${PATH}" HELM_INSTALL_DIR="${HOME}/.local/bin" bash
# Just to test that everything was put at the right place
