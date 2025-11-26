return {
  "neovim/nvim-lspconfig",
  opts = {
    servers = {
      ltex_plus = { -- or ltex_plus if you are using that specific server name
        settings = {
          ltex = {
            checkFrequency = "save", -- This is the key setting
            -- You can add other settings here, such as enabled filetypes:
            enabled = { "markdown", "tex", "latex", "text" },
            -- language = "en-US",
          },
        },
      },
    },
  },
}
