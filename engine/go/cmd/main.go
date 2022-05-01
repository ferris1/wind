package main

import (
	"wind/wnet"
)
func main(){
	s:=wnet.NewNetServer()
	s.Serve()
}

