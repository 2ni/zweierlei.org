#!/usr/bin/osascript
-- https://medium.com/@sunskyearthwind/iterm-applescript-and-jumping-quickly-into-your-workflow-1849beabb5f7
-- https://www.iterm2.com/documentation-scripting.html
-- https://stackoverflow.com/questions/48435951/how-to-write-text-to-a-iterm2-session-in-applescript

tell application "iTerm2"
  tell current tab of current window
    #set mysession to first item of sessions
    set _mysession to current session
  end tell

  tell first session of current tab of current window
    set name to "bash"
    write text "cd frontend/src; clear"
  end tell

  tell current window
    create tab with default profile
  end tell

  tell first session of current tab of current window
    write text "cd frontend/src; clear"
  end tell

  create window with default profile
  create tab with default profile

  tell first session of current tab of current window
    set name to "Node"
    set background color to {65535, 65535, 32768}
    split horizontally with default profile
    write text "cd frontend; npm run serve"
  end tell

  tell second session of current tab of current window
    set name to "Database"
    write text "cd ~/Downloads"
  end tell

#  tell _mysession
#    activate
#    select
#    #set frontmost of window id _my to true
#    write text "echo 'foo'"
#  end tell
end tell

tell application "System Events" to tell process "iTerm2"
  set frontmost to true
  windows where title contains "bash"
  if result is not {} then perform action "AXRaise" of item 1 of result
end tell
