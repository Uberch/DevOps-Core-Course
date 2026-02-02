package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net"
	"net/http"
	"os"
	"runtime"
	"time"
)

// Structures for various information
type Service struct {
	Name        string `json:"name"`
	Version     string `json:"version"`
	Description string `json:"description"`
}

type System struct {
	Hostname     string `json:"hostname"`
	Platform     string `json:"platform"`
	Architecture string `json:"architecture"`
	GoVersion    string `json:"go_version"`
	CPUCount     int    `json:"cpu_count"`
}

type Runtime struct {
	UptimeSeconds int    `json:"uptime_seconds"`
	UptimeHuman   string `json:"uptime_human"`
	CurrentTime   string `json:"current_time"`
	Timezone      string `json:"timezone"`
}

type Request struct {
	ClientIP  string `json:"client_ip"`
	UserAgent string `json:"user_agent"`
	Method    string `json:"method"`
	Path      string `json:"path"`
}

type Endpoint struct {
	Path        string `json:"path"`
	Method      string `json:"method"`
	Description string `json:"description"`
}

type ServiceInfo struct {
	Service   Service    `json:"service"`
	System    System     `json:"system"`
	Runtime   Runtime    `json:"runtime"`
	Request   Request    `json:"request"`
	Endpoints []Endpoint `json:"endpoints"`
}

type HealthInfo struct {
	Status        string `json:"status"`
	Timestamp     string `json:"timestamp"`
	UptimeSeconds int    `json:"uptime_seconds"`
}

// Helper functions for information collecting
func getSystemInfo() System {
	host, err := os.Hostname()
	if err != nil {
		DebugLogger.Print(err)
	}
	return System{
		Hostname:     host,
		Platform:     runtime.GOOS,
		Architecture: runtime.GOARCH,
		GoVersion:    runtime.Version(),
		CPUCount:     runtime.NumCPU(),
	}
}

func getUptime() Runtime {
	seconds := int(time.Since(startTime).Seconds())
	zoneName, _ := startTime.Zone()
	return Runtime{
		UptimeSeconds: seconds,
		UptimeHuman:   fmt.Sprintf("%d hours, %d minutes", seconds/3600, (seconds%3600)/60),
		CurrentTime:   time.Now().Format(time.RFC3339),
		Timezone:      zoneName,
	}
}

var Endpoints = []Endpoint{{
	Path:        "/",
	Method:      "GET",
	Description: "Service information",
}, {
	Path:        "/health",
	Method:      "GET",
	Description: "Health check",
},
}

// Handlers for http requests
func rootHandler(w http.ResponseWriter, r *http.Request) {
	DebugLogger.Printf("Request: %s %s\n", r.Method, r.URL.Path)
	log.Println("Collecting service information")
	ip, _, err := net.SplitHostPort(r.RemoteAddr)
	if err != nil {
		DebugLogger.Println("Failed to parse address, returning raw one")
		ip = r.RemoteAddr
	}
	info := ServiceInfo{
		Service: Service{
			Name:        "Info Service",
			Version:     "0.0.1",
			Description: "Simple service to collect some info",
		},

		System:  getSystemInfo(),
		Runtime: getUptime(),

		Request: Request{
			ClientIP:  ip,
			UserAgent: r.UserAgent(),
			Method:    r.Method,
			Path:      r.URL.Path,
		},
		Endpoints: Endpoints,
	}

	log.Println("Sending service information")

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(info)
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	DebugLogger.Printf("Request: %s %s\n", r.Method, r.URL.Path)
	log.Println("Collecting service health information")

	uptime := getUptime()
	info := HealthInfo{
		Status:        "healthy",
		Timestamp:     uptime.CurrentTime,
		UptimeSeconds: uptime.UptimeSeconds,
	}

	log.Println("Sending service health information")

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(info)
}

// Application istelf
var (
	startTime   = time.Now()
	DebugLevel  int
	DebugBuffer bytes.Buffer
	DebugLogger = log.New(&DebugBuffer, "Debug: ", log.Lshortfile)
)

func main() {
	log.Println("Starting application...")
	port := os.Getenv("PORT")
	if port == "" {
		port = "8000"
	}

	debug := os.Getenv("DEBUG")
	if debug == "true" {
		DebugLevel = 1
	}

	http.HandleFunc("/", rootHandler)
	http.HandleFunc("/health", healthHandler)

	log.Println("Starting server on port " + port)
	go func() {
		err := http.ListenAndServe(":"+port, nil)
		log.Println(err)
	}()
	var stop string
	fmt.Println("Type in the 'stop' to terminate")
	fmt.Scan(&stop)
	for stop!="stop"{
		fmt.Scan(&stop)
	}
	if DebugLevel>0{
		fmt.Print(&DebugBuffer)
	}
	log.Println("Terminating server")
}
