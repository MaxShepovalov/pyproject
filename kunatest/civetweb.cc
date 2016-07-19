/////////////////////////////////////////////////////////////////////////////
//
// @file  civetweb_test.cc
//
// @brief Mocked civetweb library for Unit tests
//
// @copy  Copyright 2016 Kuna Systems Corporation. All rights reserved.
//
/////////////////////////////////////////////////////////////////////////////

#include <civetweb.h>
#include <stdio.h>
#include <stddef.h>

/*              SERVER
 ****************************************************************************
 */ 

//SERVER SETUP FUNCTIONS

 int mg_set_info(struct mg_connection* conn, const void *buf, size_t len){
    free(server_out);
    memcpy(server_out, buf, len);
 }

/*              FUNCTIONS
 ****************************************************************************
 */

int mg_printf(struct mg_connection* conn, const char *format, ...){
    int output;
    //transform formatted input to string
    char* str;
    asprintf(str, const char *format, ...);
    output = mg_write(conn, str, strlen(str))
    return output;
}

int mg_write(struct mg_connection* conn, const void *buf, size_t len){
    bool status = len;
    free(server_in);
    //copy value from buffer to connection
    if (memcpy(server_in, buf, len) == NULL){
        status = -1
    }
    return status;
}

int mg_read(struct mg_connection* conn, void *buf, size_t len){
    //copy value from connection to buffer
    memcpy(buf, server_out, len);
}

struct mg_request_info* mg_get_request_info(struct mg_connection* conn){
    struct mg_request_info output;
    output.request_method = server_method;
    return &output;
}

void make_info(char* method, void* msg){
    server_method = method;
    mg_write(NULL, msg, strlen(msg));
}