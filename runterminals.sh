#!/usr/bin/osascript
-- https://medium.com/@sunskyearthwind/iterm-applescript-and-jumping-quickly-into-your-workflow-1849beabb5f7
-- https://www.iterm2.com/documentation-scripting.html

tell application "iTerm2"
  create window with default profile
  create tab with default profile

  tell first session of current tab of current window
    split horizontally with default profile
    write text "pwd"
  end tell

  tell second session of current tab of current window
    write text "cd ~/Downloads"
  end tell
end tell

tell application "iTerm2"
  tell current window
    create tab with default profile
  end tell

  tell first session of current tab of current window
    write text "echo 'hello'"
  end tell
end tell
