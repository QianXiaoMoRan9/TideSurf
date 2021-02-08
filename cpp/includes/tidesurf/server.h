#pragma once
#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#define LISTEN_PORT 8080

namespace tidesurf
{

    void start_server();
} // namespace tidesurf