local keymaps = require "config.keymaps"

return {
  {
    --addd html preview
    "turbio/bracey.vim",
    run = "cd app && yarn install",
    cmd = "Bracey",
  },
  {
    --add markdown preview
    "iamcco/markdown-preview.nvim",
    run = "cd app && yarn install",
    filetypes = { "markdown" },
    config = function()
      require("markdown-preview").setup {}
    end,
  },
}
