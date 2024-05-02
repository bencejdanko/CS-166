package main

import (
	"context"
	"crypto/tls"
	"fmt"
	"net"
	"net/http"
)

func main() {
	certFile := "example.com+4.pem"
	keyFile := "example.com+4-key.pem"

	config := &tls.Config{
		MinVersion: tls.VersionTLS12,
	}

	cert, err := tls.LoadX509KeyPair(certFile, keyFile)
	if err != nil {
		panic(err)
	}

	config.Certificates = []tls.Certificate{cert}

	server := &http.Server{
		Addr:      ":8080",
		TLSConfig: config,
		ConnContext: func(ctx context.Context, c net.Conn) context.Context {
			tc := c.(*tls.Conn)

			return context.WithValue(ctx, "tlsUnique",
				tc.ConnectionState().TLSUnique)
		},
	}

	http.HandleFunc("/unique", getTLSUniqueValueHandler)

	err = server.ListenAndServeTLS("", "")
	if err != nil {
		panic(err)
	}
}

func getTLSUniqueValueHandler(w http.ResponseWriter, r *http.Request) {
	tlsUnique, ok := r.Context().Value("tlsUnique").([]byte)
	if !ok {
		print("tlsUnique not found in context or type assertion failed")
		return
	}
	fmt.Printf("UniqueTLS: %x\n", tlsUnique)
}

// func generateUniqueTLSToken(w http.ResponseWriter, r *http.Request) {
// 	// Generate a unique token
// 	tlsUnique := getTLSUniqueValue(r)
// 	token := generateToken(tlsUnique)

// 	// Send the token back to the client
// 	w.Write([]byte(token))
// }

// func generateToken(tlsUnique []byte) string {
// 	// Your token generation logic using TLS-Unique value
// 	return "random_token_generated"
// }

// func getTLSUniqueValue(r *http.Request) []byte {
// 	tlsConnState, ok := r.TLS.(*tls.ConnectionState)
// 	if !ok {
// 		fmt.Println("TLS connection state not available")
// 		return nil
// 	}
// 	return tlsConnState.TLSUnique
// }
