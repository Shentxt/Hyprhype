return {

  -- Load File
  {
    "lervag/vimtex",
    lazy = false,
    ft = "tex",
    init = function()
    vim.g.vimtex_view_method = "zathura"
    end,
  },

  -- Formating
  {
    "stevearc/conform.nvim",
    opts = require "configs.conform",
  },

  -- Extra (Load Dependencies)
  {
  },

  -- Service (LPS)
  {
    "neovim/nvim-lspconfig",
    config = function()
      require "configs.lspconfig"
    end,
  },
}
