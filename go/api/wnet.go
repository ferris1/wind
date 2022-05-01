package api

// Server serves api requests
type Wnet interface {
	NetStart() error
	NetStop() error
}

