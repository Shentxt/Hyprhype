-- This file is automatically loaded by lazyvim.config.init

local function augroup(name)
  return vim.api.nvim_create_augroup("lazyvim_" .. name, { clear = true })
end

-- Check if we need to reload the file when it changed
vim.api.nvim_create_autocmd({ "FocusGained", "TermClose", "TermLeave" }, {
  group = augroup("checktime"),
  command = "checktime",
})

-- use vim command to be able to update the init file
vim.api.nvim_command("augroup auto_reload")
vim.api.nvim_command("  autocmd!")

-- verifies that the file is in the specified one and ends the script

vim.api.nvim_command("  autocmd BufWritePost ~/.config/nvim/**/*.lua source %") -- use your dir
vim.api.nvim_command("augroup END")
