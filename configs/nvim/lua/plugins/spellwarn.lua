return {
  "ravibrock/spellwarn.nvim",
  event = { "BufReadPre", "BufNewFile" },
  config = function()
    require("spellwarn").setup({
      enable = true,
      ft_default = false, -- we manually choose which filetypes
      ft_include = {
        "tex",
        "markdown",
        "text",
      },
      severity = {
        spellbad = "WARN",
        spellcap = "HINT",
        spelllocal = "HINT",
        spellrare = "INFO",
      },
    })

    -- Enable built-in spell options for the same filetypes
    vim.api.nvim_create_autocmd("FileType", {
      pattern = { "tex", "markdown", "text" },
      callback = function()
        vim.opt_local.spell = true
        vim.opt_local.spelllang = { "en_us" }
      end,
    })
  end,
}
