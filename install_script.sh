#!/usr/bin/env bash
set -e

INSTALL_DIR="/opt"
if [ -z "$APP_NAME" ]; then
  APP_NAME="gatekeeper"
fi
APP_DIR="$INSTALL_DIR/$APP_NAME"
DATA_DIR="/var/lib/$APP_NAME"
COMPOSE_FILE="$APP_DIR/docker-compose.yaml"

colorized_echo() {
  local color=$1
  local text=$2

  case $color in
  "red")
    printf "\e[91m${text}\e[0m\n"
    ;;
  "green")
    printf "\e[92m${text}\e[0m\n"
    ;;
  "yellow")
    printf "\e[93m${text}\e[0m\n"
    ;;
  "blue")
    printf "\e[94m${text}\e[0m\n"
    ;;
  "magenta")
    printf "\e[95m${text}\e[0m\n"
    ;;
  "cyan")
    printf "\e[96m${text}\e[0m\n"
    ;;
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
  detect_os
  if [[ "$OS" == "Ubuntu"* ]] || [[ "$OS" == "Ubuntu Linux"* ]] || [[ "$OS" == "Debian"* ]]; then
    PKG_MANAGER="apt-get"
    $PKG_MANAGER update
  elif [[ "$OS" == "CentOS"* ]] || [[ "$OS" == "AlmaLinux"* ]]; then
    PKG_MANAGER="yum"
    $PKG_MANAGER update -y
    $PKG_MANAGER install -y epel-release
  elif [ "$OS" == "Fedora"* ] || [[ "$OS" == "Fedora Linux"* ]]; then
    PKG_MANAGER="dnf"
    $PKG_MANAGER update -y
  elif [ "$OS" == "Arch" ]; then
    PKG_MANAGER="pacman"
    $PKG_MANAGER -Sy
  else
    colorized_echo red "Unsupported operating system"
    exit 1
  fi
}

detect_compose() {
  if docker compose >/dev/null 2>&1; then
    COMPOSE='docker compose'
  elif docker-compose >/dev/null 2>&1; then
    COMPOSE='docker-compose'
  else
    colorized_echo red "docker compose not found"
    exit 1
  fi
}

install_package() {
  if [ -z $PKG_MANAGER ]; then
    detect_and_update_package_manager
  fi

  PACKAGE=$1
  colorized_echo blue "Installing $PACKAGE"
  if [[ "$OS" == "Ubuntu"* ]] || [[ "$OS" == "Ubuntu Linux"* ]] || [[ "$OS" == "Debian"* ]]; then
    $PKG_MANAGER -y install "$PACKAGE"
  elif [[ "$OS" == "CentOS"* ]] || [[ "$OS" == "AlmaLinux"* ]]; then
    $PKG_MANAGER install -y "$PACKAGE"
  elif [[ "$OS" == "Fedora"* ]]; then
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
  FETCH_REPO="drunkleen/gatekeeper"
  SCRIPT_URL="https://github.com/$FETCH_REPO/raw/master/install_script.sh"
  colorized_echo blue "Installing Gate-Keeper script"
  curl -sSL $SCRIPT_URL | install -m 755 /dev/stdin /usr/local/bin/gatekeeper
  colorized_echo green "Gate-Keeper script installed successfully"
}

install_gatekeeper() {
  FILES_URL_PREFIX="https://raw.githubusercontent.com/drunkleen/gatekeeper/master"

  mkdir -p "$DATA_DIR"
  mkdir -p "$APP_DIR"

  colorized_echo blue "Fetching compose file"
  curl -sL "$FILES_URL_PREFIX/docker-compose.yaml" -o "$APP_DIR/docker-compose.yaml"
  colorized_echo green "File saved in $APP_DIR/docker-compose.yaml"

  colorized_echo blue "Fetching .env file"
  curl -sL "$FILES_URL_PREFIX/.env.example" -o "$APP_DIR/.env"
  colorized_echo green "File saved in $APP_DIR/.env"

  colorized_echo green "GateKeeper files downloaded successfully"
}

uninstall_gatekeeper_script() {
  if [ -f "/usr/local/bin/gatekeeper" ]; then
    colorized_echo yellow "Removing GateKeeper script"
    rm "/usr/local/bin/gatekeeper"
  fi
}

uninstall_gatekeeper() {
  if [ -d "$APP_DIR" ]; then
    colorized_echo yellow "Removing directory: $APP_DIR"
    rm -r "$APP_DIR"
  fi
}

uninstall_gatekeeper_docker_images() {
  images=$(docker images | grep gatekeeper | awk '{print $3}')

  if [ -n "$images" ]; then
    colorized_echo yellow "Removing Docker images of GateKeeper"
    for image in $images; do
      if docker rmi "$image" >/dev/null 2>&1; then
        colorized_echo yellow "Image $image removed"
      fi
    done
  fi
}

uninstall_gatekeeper_data_files() {
  if [ -d "$DATA_DIR" ]; then
    colorized_echo yellow "Removing directory: $DATA_DIR"
    rm -r "$DATA_DIR"
  fi
}

up_gatekeeper() {
  $COMPOSE -f $COMPOSE_FILE -p "$APP_NAME" up -d --remove-orphans
}

down_gatekeeper() {
  $COMPOSE -f $COMPOSE_FILE -p "$APP_NAME" down
}

show_gatekeeper_logs() {
  $COMPOSE -f $COMPOSE_FILE -p "$APP_NAME" logs
}

follow_gatekeeper_logs() {
  $COMPOSE -f $COMPOSE_FILE -p "$APP_NAME" logs -f
}

update_gatekeeper_script() {
  FETCH_REPO="drunkleen/gatekeeper"
  SCRIPT_URL="https://github.com/$FETCH_REPO/raw/master/install_script.sh"
  colorized_echo blue "Updating Gate-Keeper script"
  curl -sSL $SCRIPT_URL | install -m 755 /dev/stdin /usr/local/bin/gatekeeper
  colorized_echo green "Gate-Keeper script updated successfully"
}

update_gatekeeper() {
  $COMPOSE -f $COMPOSE_FILE -p "$APP_NAME" pull
}

is_gatekeeper_installed() {
  if [ -d $APP_DIR ]; then
    return 0
  else
    return 1
  fi
}

is_gatekeeper_up() {
  if [ -z "$($COMPOSE -f $COMPOSE_FILE ps -q -a)" ]; then
    return 1
  else
    return 0
  fi
}

install_command() {
  check_running_as_root

  if is_gatekeeper_installed; then
    colorized_echo red "GateKeeper is already installed at $APP_DIR"
    read -p "Do you want to override the previous installation? (y/n) "
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
      colorized_echo red "Aborted installation"
      exit 1
    fi
  fi
  detect_os
  if ! command -v jq >/dev/null 2>&1; then
    install_package jq
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
  up_gatekeeper
  follow_gatekeeper_logs
}

createadmin() {
  docker exec -it $APP_NAME sh -c "cd /app/ && python ./cli.py createadmin"
}

open_shell() {
  docker exec -it $APP_NAME sh -c "cd /app/ && python ./cli.py shell"
}

uninstall_command() {
  check_running_as_root
  if ! is_gatekeeper_installed; then
    colorized_echo red "GateKeeper not installed!"
    exit 1
  fi

  read -p "Do you really want to uninstall GateKeeper? (y/n) "
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    colorized_echo red "Aborted"
    exit 1
  fi

  detect_compose
  if is_gatekeeper_up; then
    down_gatekeeper
  fi
  uninstall_gatekeeper_script
  uninstall_gatekeeper
  uninstall_gatekeeper_docker_images

  read -p "Do you want to remove GateKeeper data files too ($DATA_DIR)? (y/n) "
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    colorized_echo green "GateKeeper uninstalled successfully"
  else
    uninstall_gatekeeper_data_files
    colorized_echo green "GateKeeper uninstalled successfully"
  fi
}

up_command() {
  help() {
    colorized_echo red "Usage: GateKeeper up [options]"
    echo ""
    echo "OPTIONS:"
    echo "  -h, --help        display this help message"
    echo "  -n, --no-logs     do not follow logs after starting"
  }

  local no_logs=false
  while [[ "$#" -gt 0 ]]; do
    case "$1" in
    -n | --no-logs)
      no_logs=true
      ;;
    -h | --help)
      help
      exit 0
      ;;
    *)
      echo "Error: Invalid option: $1" >&2
      help
      exit 0
      ;;
    esac
    shift
  done

  if ! is_gatekeeper_installed; then
    colorized_echo red "GateKeeper not installed!"
    exit 1
  fi

  detect_compose

  if is_gatekeeper_up; then
    colorized_echo red "GateKeeper already up"
    exit 1
  fi

  up_gatekeeper
  if [ "$no_logs" = false ]; then
    follow_gatekeeper_logs
  fi
}

down_command() {
  if ! is_gatekeeper_installed; then
    colorized_echo red "GateKeeper not installed!"
    exit 1
  fi

  detect_compose

  if ! is_gatekeeper_up; then
    colorized_echo red "GateKeeper already down"
    exit 1
  fi

  down_gatekeeper
}

restart_command() {
  help() {
    colorized_echo red "Usage: GateKeeper restart [options]"
    echo
    echo "OPTIONS:"
    echo "  -h, --help        display this help message"
    echo "  -n, --no-logs     do not follow logs after starting"
  }

  local no_logs=false
  while [[ "$#" -gt 0 ]]; do
    case "$1" in
    -n | --no-logs)
      no_logs=true
      ;;
    -h | --help)
      help
      exit 0
      ;;
    *)
      echo "Error: Invalid option: $1" >&2
      help
      exit 0
      ;;
    esac
    shift
  done

  if ! is_gatekeeper_installed; then
    colorized_echo red "GateKeeper not installed!"
    exit 1
  fi

  detect_compose

  down_gatekeeper
  up_gatekeeper
  if [ "$no_logs" = false ]; then
    follow_gatekeeper_logs
  fi
}

status_command() {

  if ! is_gatekeeper_installed; then
    echo -n "Status: "
    colorized_echo red "Not Installed"
    exit 1
  fi

  detect_compose

  if ! is_gatekeeper_up; then
    echo -n "Status: "
    colorized_echo blue "Down"
    exit 1
  fi

  echo -n "Status: "
  colorized_echo green "Up"

  json=$($COMPOSE -f $COMPOSE_FILE ps -a --format=json)
  services=$(echo "$json" | jq -r 'if type == "array" then .[] else . end | .Service')
  states=$(echo "$json" | jq -r 'if type == "array" then .[] else . end | .State')

  for i in $(seq 0 $(expr $(echo $services | wc -w) - 1)); do
    service=$(echo $services | cut -d' ' -f $(expr $i + 1))
    state=$(echo $states | cut -d' ' -f $(expr $i + 1))
    echo -n "- $service: "
    if [ "$state" == "running" ]; then
      colorized_echo green $state
    else
      colorized_echo red $state
    fi
  done
}

logs_command() {
  help() {
    colorized_echo red "Usage: GateKeeper logs [options]"
    echo ""
    echo "OPTIONS:"
    echo "  -h, --help        display this help message"
    echo "  -n, --no-follow   do not show follow logs"
  }

  local no_follow=false
  while [[ "$#" -gt 0 ]]; do
    case "$1" in
    -n | --no-follow)
      no_follow=true
      ;;
    -h | --help)
      help
      exit 0
      ;;
    *)
      echo "Error: Invalid option: $1" >&2
      help
      exit 0
      ;;
    esac
    shift
  done

  if ! is_gatekeeper_installed; then
    colorized_echo red "GateKeeper not installed!"
    exit 1
  fi

  detect_compose

  if ! is_gatekeeper_up; then
    colorized_echo red "GateKeeper is not up."
    exit 1
  fi

  if [ "$no_follow" = true ]; then
    show_gatekeeper_logs
  else
    follow_gatekeeper_logs
  fi
}

update_command() {
  check_running_as_root
  if ! is_gatekeeper_installed; then
    colorized_echo red "GateKeeper not installed!"
    exit 1
  fi

  detect_compose

  update_gatekeeper_script
  colorized_echo blue "Pulling latest version"
  update_gatekeeper

  colorized_echo blue "Restarting GateKeeper services"
  down_gatekeeper
  up_gatekeeper

  colorized_echo blue "GateKeeper updated successfully"
}

usage() {
  colorized_echo red "Usage: GateKeeper [command]"
  echo
  echo "Commands:"
  echo "  up              Start services"
  echo "  down            Stop services"
  echo "  restart         Restart services"
  echo "  status          Show status"
  echo "  logs            Show logs"
  echo "  createadmin     Creates an admin account"
  echo "  shell           Open GateKeeper Shell"
  echo "  install         Install GateKeeper"
  echo "  update          Update latest version"
  echo "  uninstall       Uninstall GateKeeper"
  echo "  install-script  Install GateKeeper script"
  echo
}

case "$1" in
up)
  shift
  up_command "$@"
  ;;
down)
  shift
  down_command "$@"
  ;;
restart)
  shift
  restart_command "$@"
  ;;
status)
  shift
  status_command "$@"
  ;;
logs)
  shift
  logs_command "$@"
  ;;
createadmin)
  shift
  createadmin "$@"
  ;;
shell)
  shift
  open_shell "$@"
  ;;
install)
  shift
  install_command "$@"
  ;;
update)
  shift
  update_command "$@"
  ;;
uninstall)
  shift
  uninstall_command "$@"
  ;;
install-script)
  shift
  install_gatekeeper_script "$@"
  ;;
*)
  usage
  ;;
esac
