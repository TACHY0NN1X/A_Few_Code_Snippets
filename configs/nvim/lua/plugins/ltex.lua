-- lua/plugins/ltex.lua
return {
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
        ltex = {
          cmd = { "ltex-ls-plus" },
          filetypes = { "tex", "bib", "markdown" },
          settings = {
            ltex = {
              language = "en-GB", -- or "en-US"
              checkFrequency = "save", -- Checks on Save

              additionalRules = {
                enablePickyRules = true,
                motherTongue = "en",
              },

              dictionary = {
                ["en-US"] = { "neovim", "vimtex", "LazyVim" },
              },
            },
          },
        },
      },
    },
  },
}
