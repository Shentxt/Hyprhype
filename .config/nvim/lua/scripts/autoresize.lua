-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
--
-- Autor = Shen Blaskowitz
-- Inpiracions = https://github.com/LazyVim/LazyVim
-- Followme = https://github.com/Shentxt
--
--  █████╗ ██╗   ██╗████████╗ ██████╗ ██████╗ ███████╗███████╗██╗███████╗███████╗
-- ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗██╔══██╗██╔════╝██╔════╝██║╚══███╔╝██╔════╝
-- ███████║██║   ██║   ██║   ██║   ██║██████╔╝█████╗  ███████╗██║  ███╔╝ █████╗  
-- ██╔══██║██║   ██║   ██║   ██║   ██║██╔══██╗██╔══╝  ╚════██║██║ ███╔╝  ██╔══╝  
-- ██║  ██║╚██████╔╝   ██║   ╚██████╔╝██║  ██║███████╗███████║██║███████╗███████╗
-- ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚══════╝╚══════╝
--
-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
--                 Auto Reload Init
--
-- a simple setup to automatically reload line highlight
--
-- read for more information
-- - - - - - - - - - - - - -
-- wiki: https://vi.stackexchange.com/questions/38722/are-vim-cmd-and-vim-api-nvim-command-the-same-if-not-what-are-the-differen
-- wiki: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/autocmds.lua
--
-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

-- This file is automatically loaded by lazyvim.config.init

local function augroup(name)
  return vim.api.nvim_create_augroup("lazyvim_" .. name, { clear = true })
end

-- resize splits if window got resized
vim.api.nvim_create_autocmd({ "VimResized" }, {
  group = augroup("resize_splits"),
  callback = function()
    vim.cmd("tabdo wincmd =")
  end,
})
