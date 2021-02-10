#pragma once
#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#include <pthread.h>
#define LISTEN_PORT 8080

namespace tidesurf
{

    void start_server();
    class ClientInfo
    {
    public:
        struct sockaddr_in socket_address_;
        socklen_t socket_address_length_;
        int connection_fd_;
        char *host_info_;
        char *service_info_;
        ClientInfo()
        {
            socket_address_length_ = sizeof(struct sockaddr_in);
        }
    };

    class DashboardServer
    {

    public:
        DashboardServer(int listen_port);

        /**
 * @brief Initialize Socket settings
 * 
 */
        void InitServer();

        /**
 * @brief Start the server listening loop to listen for clients
 * 
 */
        void StartServer();

    private:
        int listen_port_, socket_option_, server_fd_;
        struct sockaddr_in address_;
    };
    
    
} // namespace tidesurf