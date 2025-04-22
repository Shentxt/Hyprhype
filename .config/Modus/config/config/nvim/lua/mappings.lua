require "nvchad.mappings"

local map = vim.keymap.set

map("n", ";", ":", { desc = "CMD enter command mode" })
map("i", "jk", "<ESC>")

-- Open Preview (Latex, Markdown and html)
map("n", "<C-l>", function()
  if vim.bo.filetype == "tex" then
    vim.cmd("VimtexCompile")
    vim.cmd("sleep 1")
    vim.cmd("VimtexView")
  end
end, { noremap = true, silent = true, desc = "Compile and view LaTeX PDF" })
