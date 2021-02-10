#include "tidesurf/dashboard_server.h"

using namespace tidesurf;

void *serve_thread(void *vargp) {
        pthread_exit(NULL);
    }

void start_server()
{

    int server_fd, new_socket, valread;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char buffer[1024] = {0};
    const char *hello = "Hello from server";

    // Creating socket file descriptor
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0)
    {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    // Forcefully attaching socket to the port 8080
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT,
                   &opt, sizeof(opt)))
    {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(LISTEN_PORT);

    // Forcefully attaching socket to the port 8080
    if (bind(server_fd, (struct sockaddr *)&address,
             sizeof(address)) < 0)
    {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }
    if (listen(server_fd, 3) < 0)
    {
        perror("listen");
        exit(EXIT_FAILURE);
    }
    if ((new_socket = accept(server_fd, (struct sockaddr *)&address,
                             (socklen_t *)&addrlen)) < 0)
    {
        perror("accept");
        exit(EXIT_FAILURE);
    }
    valread = read(new_socket, buffer, 1024);
    printf("%s\n", buffer);
    send(new_socket, hello, strlen(hello), 0);
    printf("Hello message sent\n");
}

DashboardServer::DashboardServer(int listen_port) : listen_port_(listen_port)
{
}

void DashboardServer::InitServer()
{
    socket_option_ = 1;
    // Creating socket file descriptor
    if ((server_fd_ = socket(AF_INET, SOCK_STREAM, 0)) == 0)
    {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    // Forcefully attaching socket to the port 8080
    if (setsockopt(server_fd_, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT,
                   &socket_option_, sizeof(socket_option_)))
    {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }
    address_.sin_family = AF_INET;
    address_.sin_addr.s_addr = INADDR_ANY;
    address_.sin_port = htons(LISTEN_PORT);

    // Forcefully attaching socket to the port 8080
    if (bind(server_fd_, (struct sockaddr *)&address_,
             sizeof(address_)) < 0)
    {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }
    if (listen(server_fd_, 3) < 0)
    {
        perror("listen");
        exit(EXIT_FAILURE);
    }
}

void DashboardServer::StartServer()
{
    while (true)
    {
        pthread_t tid; // init tid;
        /* Allocate space on the stack for client info */
        ClientInfo *client_info = new ClientInfo();
        /* Accept() will block until a client connects to the port */
        client_info->connection_fd_ = accept(
            server_fd_,
            (struct sockaddr *)&client_info->socket_address_, 
            (socklen_t *)&client_info->socket_address_length_);
        pthread_create(&tid, NULL, serve_thread, client_info);
    }
}



