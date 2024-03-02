#!/usr/bin/env bash
set -e

INSTALL_DIR="/opt"

if [ -z "$APP_NAME" ]; then
    APP_NAME="gatekeeper"
fi

APP_DIR="$INSTALL_DIR/$APP_NAME"
DATA_DIR="/var/lib/$APP_NAME"



colorized_echo() {
  local color=$1
  local text=$2

  case $color in
    "red")
    printf "\e[91m${text}\e[0m\n";;
    "green")
    printf "\e[92m${text}\e[0m\n";;
    "yellow")
    printf "\e[93m${text}\e[0m\n";;
    "blue")
    printf "\e[94m${text}\e[0m\n";;
    "magenta")
    printf "\e[95m${text}\e[0m\n";;
    "cyan")
    printf "\e[96m${text}\e[0m\n";;
    *)
      echo "${text}"
    ;;
  esac
}


check_running_as_root() {
  if [ "$(id -u)" != "0" ]; then
    colorized_echo red "This command must be run as root."
    exit 1
  fi
}


# Detect the operating system
detect_os() {
  if [ -f /etc/lsb-release ]; then
    OS=$(lsb_release -si)
    elif [ -f /etc/os-release ]; then
    OS=$(awk -F= '/^NAME/{print $2}' /etc/os-release | tr -d '"')
    elif [ -f /etc/redhat-release ]; then
    OS=$(cat /etc/redhat-release | awk '{print $1}')
    elif [ -f /etc/arch-release ]; then
    OS="Arch"
  else
    colorized_echo red "Unsupported operating system"
    exit 1
  fi
}


detect_and_update_package_manager() {
  colorized_echo blue "Updating package manager"
  if [[ "$OS" == "Ubuntu"* ]] || [[ "$OS" == "Debian"* ]]; then
    PKG_MANAGER="apt-get"
    $PKG_MANAGER update
    elif [[ "$OS" == "CentOS"* ]] || [[ "$OS" == "AlmaLinux"* ]]; then
    PKG_MANAGER="yum"
    $PKG_MANAGER update -y
    $PKG_MANAGER install -y epel-release
    elif [ "$OS" == "Fedora"* ]; then
    PKG_MANAGER="dnf"
    $PKG_MANAGER update
    elif [ "$OS" == "Arch" ]; then
    PKG_MANAGER="pacman"
    $PKG_MANAGER -Sy
  else
    colorized_echo red "Unsupported operating system"
    exit 1
  fi
}


detect_compose() {
  # Check if docker compose command exists
  if docker compose >/dev/null 2>&1; then
    COMPOSE='docker compose'
    elif docker-compose >/dev/null 2>&1; then
    COMPOSE='docker-compose'
  else
    colorized_echo red "docker compose not found"
    exit 1
  fi
}


install_package () {
  if [ -z $PKG_MANAGER ]; then
    detect_and_update_package_manager
  fi

  PACKAGE=$1
  colorized_echo blue "Installing $PACKAGE"
  if [[ "$OS" == "Ubuntu"* ]] || [[ "$OS" == "Debian"* ]]; then
    $PKG_MANAGER -y install "$PACKAGE"
    elif [[ "$OS" == "CentOS"* ]] || [[ "$OS" == "AlmaLinux"* ]]; then
    $PKG_MANAGER install -y "$PACKAGE"
    elif [ "$OS" == "Fedora"* ]; then
    $PKG_MANAGER install -y "$PACKAGE"
    elif [ "$OS" == "Arch" ]; then
    $PKG_MANAGER -S --noconfirm "$PACKAGE"
  else
    colorized_echo red "Unsupported operating system"
    exit 1
  fi
}


install_docker() {
  colorized_echo blue "Installing Docker"
  curl -fsSL https://get.docker.com | sh
  colorized_echo green "Docker installed successfully"
}


install_gatekeeper_script() {
  FETCH_REPO="drunkleen/Gate-Keeper"
  SCRIPT_URL="https://github.com/$FETCH_REPO/raw/master/install_script.sh"
  colorized_echo blue "Installing Gate-Keeper script"
  curl -sSL $SCRIPT_URL | install -m 755 /dev/stdin /usr/local/bin/gatekeeper
  colorized_echo green "Gate-Keeper script installed successfully"
}


install_gatekeeper() {
  GK_REPO = "https://github.com/drunkleen/Gate-Keeper"

  mkdir -p "$DATA_DIR"
  mkdir -p "$APP_DIR"

  git clone $GK_REPO $APP_DIR
  colorized_echo green "Gate-Keeper Project saved in $APP_DIR"

  $COMPOSE -f "$APP_DIR/docker-compose.yml" -p "$APP_NAME" up --build --remove-orphans -d

  $COMPOSE -f "$APP_DIR/docker-compose.yml" -p "$APP_NAME" logs -f

  colorized_echo green "Gate-Keeper installed and running successfully"
}


install_command() {
    check_running_as_root

    detect_os
    if ! command -v jq >/dev/null 2>&1; then
        install_package jq
    fi
    if ! command -v git >/dev/null 2>&1; then
        install_package git
    fi
    if ! command -v curl >/dev/null 2>&1; then
        install_package curl
    fi
    if ! command -v docker >/dev/null 2>&1; then
        install_docker
    fi
    detect_compose
    install_gatekeeper_script
    install_gatekeeper
}

sudo mv $APP_DIR/install_script.sh /usr/local/bin/gatekeeper





