#!/bin/sh
set -eu

APP_DIR="/app"
ENV_FILE="/tmp/.env"
HOST_REQUIREMENTS_FILE="/tmp/host_requirements.txt"
HOST_SRC_DIR="/tmp/host_src"
HOST_TEST_DIR="/tmp/host_test"

if [ ! -f "${ENV_FILE}" ]; then
    echo ".env not found"
    exit 1
fi

set -a
. "${ENV_FILE}"
set +a

if [ -z "${GIT_USERNAME:-}" ] || [ -z "${GIT_TOKEN:-}" ] || [ -z "${GIT_REPO_HOST:-}" ] || [ -z "${GIT_REPO_URL:-}" ]; then
    echo "GIT_USERNAME/GIT_TOKEN/GIT_REPO_HOST/GIT_REPO_URL must be set in .env"
    exit 1
fi

REPO_PATH="/${GIT_REPO_URL#/}"
case "${REPO_PATH}" in
    *.git) ;;
    *) REPO_PATH="${REPO_PATH}.git" ;;
esac

BRANCH_NAME="${GIT_BRANCH_NAME:-master}"
AUTH_REPO_URL="https://${GIT_USERNAME}:${GIT_TOKEN}@${GIT_REPO_HOST}${REPO_PATH}"

echo "Preparing ${APP_DIR} from bundled host files"
find "${APP_DIR}" -mindepth 1 -maxdepth 1 \
    ! -name "logs" \
    -exec rm -rf {} \;

if [ -d "${HOST_SRC_DIR}" ]; then
    mkdir -p "${APP_DIR}/src"
    cp -a "${HOST_SRC_DIR}/." "${APP_DIR}/src/"
fi

if [ -d "${HOST_TEST_DIR}" ]; then
    mkdir -p "${APP_DIR}/test"
    cp -a "${HOST_TEST_DIR}/." "${APP_DIR}/test/"
fi

echo "Fetching branch ${BRANCH_NAME} into ${APP_DIR}"
git init "${APP_DIR}"
git -C "${APP_DIR}" remote remove origin 2>/dev/null || true
git -C "${APP_DIR}" remote add origin "${AUTH_REPO_URL}"
git -C "${APP_DIR}" fetch --depth 1 origin "${BRANCH_NAME}"
git -C "${APP_DIR}" reset --hard FETCH_HEAD

cp "${ENV_FILE}" "${APP_DIR}/.env"

if [ ! -f "${APP_DIR}/requirements.txt" ] && [ -f "${HOST_REQUIREMENTS_FILE}" ]; then
    cp "${HOST_REQUIREMENTS_FILE}" "${APP_DIR}/requirements.txt"
fi

if [ -f "${APP_DIR}/requirements.txt" ]; then
    pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r "${APP_DIR}/requirements.txt"
fi
