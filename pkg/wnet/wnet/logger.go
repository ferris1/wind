package wnet

import (
	"fmt"
	"time"
)

var (
	NetLog ILogger = nil
)

type ILogger interface {
	Init(srvName string) error
	Info(format string, v ...interface{})
	Warn(format string, v ...interface{})
	Erorr(format string, v ...interface{})
	Fatal(format string, v ...interface{})
}


func NewLogger() ILogger {
	return &Logger{
	}
}

type Logger struct {
	prefix string
}

func (lg *Logger) Init(srvName string) error {
	lg.prefix = fmt.Sprintf("[wind][net][%s]",srvName)
	return nil
}

func (lg *Logger) Info(format string, v ...interface{})  {
	now := time.Now().UTC()
	mid := fmt.Sprintf("[%s][INFO]: ",now.Format(DDMMYYYYhhmmss))
	fmt.Println(lg.prefix, mid, fmt.Sprintf(format,v...))
}

func (lg *Logger) Warn(format string, v ...interface{})  {
	now := time.Now().UTC()
	mid := fmt.Sprintf("[%s][Warn]: ",now.Format(DDMMYYYYhhmmss))
	fmt.Println(lg.prefix, mid, fmt.Sprintf(format,v...))
}

func (lg *Logger) Erorr(format string, v ...interface{})  {
	now := time.Now().UTC()
	mid := fmt.Sprintf("[%s][Erorr]: ",now.Format(DDMMYYYYhhmmss))
	fmt.Println(lg.prefix, mid, fmt.Sprintf(format,v...))
}

func (lg *Logger) Fatal(format string, v ...interface{})  {
	now := time.Now().UTC()
	mid := fmt.Sprintf("[%s][Fatal]: ",now.Format(DDMMYYYYhhmmss))
	fmt.Println(lg.prefix, mid, fmt.Sprintf(format,v...))
}

