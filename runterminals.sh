#!/usr/bin/osascript
-- https://medium.com/@sunskyearthwind/iterm-applescript-and-jumping-quickly-into-your-workflow-1849beabb5f7
-- https://www.iterm2.com/documentation-scripting.html
-- https://stackoverflow.com/questions/48435951/how-to-write-text-to-a-iterm2-session-in-applescript

tell application "Finder"
 set displayAreaDimensions to bounds of window of desktop
 set x1 to item 1 of displayAreaDimensions
 set y1 to item 2 of displayAreaDimensions
 set x2 to item 3 of displayAreaDimensions
 set y2 to item 4 of displayAreaDimensions

 -- get size of main screen
 -- https://stackoverflow.com/questions/1866912/applescript-how-to-get-current-display-resolution
 set dimensions to words of (do shell script "system_profiler SPDisplaysDataType | awk '/Main Display: Yes/{found=1} /Resolution/{width=$2; height=$4} /Retina/{scale=($2 == \"Yes\" ? 2 : 1)} /^ {8}[^ ]+/{if(found) {exit}; scale=1} END{printf \"%d %d %d\\n\", width, height, scale}'")
end tell

set width to item 1 of dimensions
set height to item 2 of dimensions

tell application "iTerm2"
  tell current tab of current window
    #set mysession to first item of sessions
    set _mysession to current session
  end tell

  tell first session of current tab of current window
    set name to "frontend"
    set name to "bash"
    write text "cd frontend/src; clear"
  end tell

  tell current window
    create tab with default profile
  end tell

  tell first session of current tab of current window
    set name to "backend"
    write text "cd backend; clear"
  end tell

  create window with default profile
  set the bounds of the first window to {x2 - 2*width/3, y2 - height/3, x2, y2}
  create tab with default profile


  tell first session of current tab of current window
    set name to "Node"
    set background color to {65535, 65535, 32768}
    split horizontally with default profile
    split vertically with default profile
    write text "cd frontend; npm run serve"
  end tell

  tell second session of current tab of current window
    set name to "Flask"
    set background color to {65535, 32768, 65535}
    write text "cd backend; make server"
  end tell

  tell third session of current tab of current window
    set name to "Redis"
    set background color to {32768, 65535, 65535}
    write text "redis-server /usr/local/etc/redis.conf"
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
