package main
import (
	"wnet/wnet"
)

func main(){
	s:= wnet.NewNetServer()
	s.Serve()
}

