#' PocketGull Typographic Theme for ggplot2
#'
#' Provides Louise Sloan 5:1 optotypic acuity and ISMP clinical character
#' disambiguation for clinical trials, biostatistics, and telemetry plots.
#'
#' @param base_size Base font size, default 11 pt.
#' @param base_family Base font family, default "PocketGull".
#' @param mode Theme mode: "light" or "scotopic" (650nm red night vision).
#' @return A ggplot2 theme object.
#' @export
theme_pocketgull <- function(base_size = 11, base_family = "PocketGull", mode = c("light", "scotopic")) {
  mode <- match.arg(mode)
  
  if (!requireNamespace("ggplot2", quietly = TRUE)) {
    stop("Package 'ggplot2' is required to use theme_pocketgull().", call. = FALSE)
  }
  
  if (mode == "scotopic") {
    bg_color <- "#09090b"
    text_color <- "#f43f5e"     # Scotopic 650nm clinical red
    grid_color <- "#27272a"
    axis_color <- "#e11d48"
  } else {
    bg_color <- "#ffffff"
    text_color <- "#18181b"
    grid_color <- "#f4f4f5"
    axis_color <- "#71717a"
  }
  
  ggplot2::theme_minimal(base_size = base_size, base_family = base_family) +
    ggplot2::theme(
      plot.background = ggplot2::element_rect(fill = bg_color, color = NA),
      panel.background = ggplot2::element_rect(fill = bg_color, color = NA),
      text = ggplot2::element_text(color = text_color, family = base_family),
      plot.title = ggplot2::element_text(face = "bold", size = ggplot2::rel(1.2), margin = ggplot2::margin(b = 6)),
      plot.subtitle = ggplot2::element_text(size = ggplot2::rel(0.95), margin = ggplot2::margin(b = 10)),
      axis.title = ggplot2::element_text(face = "bold", size = ggplot2::rel(0.9)),
      axis.text = ggplot2::element_text(color = text_color, size = ggplot2::rel(0.85)),
      panel.grid.major = ggplot2::element_line(color = grid_color, linewidth = 0.5),
      panel.grid.minor = ggplot2::element_blank(),
      axis.line = ggplot2::element_line(color = axis_color, linewidth = 0.6),
      legend.background = ggplot2::element_rect(fill = bg_color, color = NA),
      legend.key = ggplot2::element_rect(fill = bg_color, color = NA),
      legend.title = ggplot2::element_text(face = "bold", size = ggplot2::rel(0.85)),
      legend.text = ggplot2::element_text(size = ggplot2::rel(0.8))
    )
}

#' Register PocketGull fonts into R graphics devices
#'
#' Automatically registers PocketGull into showtext and sysfonts for
#' crisp optotypic rendering across PDF, PNG, and Cairo devices.
#'
#' @export
use_pocketgull <- function() {
  if (requireNamespace("showtext", quietly = TRUE) && requireNamespace("sysfonts", quietly = TRUE)) {
    font_dir <- system.file("fonts", package = "pocketgullr")
    if (font_dir != "" && dir.exists(font_dir)) {
      reg <- file.path(font_dir, "PocketGull-Fineliner.ttf")
      bold <- file.path(font_dir, "PocketGull-Bold.ttf")
      mono <- file.path(font_dir, "PocketGullMono-Regular.ttf")
      sysfonts::font_add("PocketGull", regular = reg, bold = bold)
      sysfonts::font_add("PocketGull Mono", regular = mono)
    } else {
      # Fallback to local system fonts if package fonts dir is empty
      sysfonts::font_add_google("Atkinson Hyperlegible", "PocketGull")
    }
    showtext::showtext_auto()
    message("PocketGull typography registered for R graphics devices.")
  } else {
    warning("Please install 'showtext' and 'sysfonts' to enable automatic PocketGull font rendering in R.")
  }
}
