#!/usr/bin/env Rscript
# Create Diagnostic Plots for WTI Data: CSS-ML vs PMM2
# This script generates comprehensive diagnostic plots for the best ARIMA(1,1,1) model

library(ggplot2)
library(gridExtra)

cat("Creating WTI diagnostic plots for CSS-ML vs PMM2...\n\n")

# Load results
output_dir <- "results"
if (!dir.exists(output_dir)) {
  stop("Results directory not found. Run comprehensive_study.R first.")
}

results <- readRDS(file.path(output_dir, "all_results.rds"))
fitted_models <- readRDS(file.path(output_dir, "fitted_models.rds"))

# Create plots directory
plots_dir <- file.path(output_dir, "plots")
if (!dir.exists(plots_dir)) {
  dir.create(plots_dir, recursive = TRUE)
}

# Find ARIMA(1,1,1) models for both methods
arima111_results <- results[results$Model == "ARIMA(1,1,1)", ]

if (nrow(arima111_results) < 2) {
  stop("ARIMA(1,1,1) results not found for both methods.")
}

# Extract fitted models (using correct keys from the error message)
cssml_fit <- fitted_models[["ARIMA(1,1,1)_CSS"]]
pmm2_fit <- fitted_models[["ARIMA(1,1,1)_PMM2"]]

if (is.null(cssml_fit) || is.null(pmm2_fit)) {
  stop("Fitted models not found. Available models: ",
       paste(names(fitted_models), collapse = ", "))
}

cat("Found ARIMA(1,1,1) models for both methods\n")

# ==================== DIAGNOSTIC PLOT: CSS-ML ====================
cat("Creating CSS-ML diagnostics... ")

# Extract CSS-ML residuals
cssml_res <- residuals(cssml_fit)
cssml_res_clean <- cssml_res[is.finite(cssml_res)]

png(file.path(plots_dir, "11_cssml_diagnostics.png"),
    width = 12, height = 10, units = "in", res = 300)

par(mfrow = c(2, 2), mar = c(4, 4, 3, 2), bg = "white")

# 1. Residuals over time
plot(cssml_res_clean, type = "l", col = "#E41A1C", lwd = 1.2,
     main = "CSS-ML: Residuals Over Time",
     xlab = "Observation Index", ylab = "Residuals",
     cex.main = 1.3, cex.lab = 1.1)
abline(h = 0, col = "black", lty = 2, lwd = 1.5)
grid(col = "gray90")

# 2. Histogram with normal overlay
hist(cssml_res_clean, breaks = 50, col = "#E41A1C80", border = "white",
     main = "CSS-ML: Histogram of Residuals",
     xlab = "Residuals", freq = FALSE,
     cex.main = 1.3, cex.lab = 1.1)
curve(dnorm(x, mean = mean(cssml_res_clean), sd = sd(cssml_res_clean)),
      add = TRUE, col = "black", lwd = 2)
# Add skewness and kurtosis
cssml_skew <- arima111_results[arima111_results$Method == "CSS-ML", "Skewness"]
cssml_kurt <- arima111_results[arima111_results$Method == "CSS-ML", "Kurtosis"]
legend("topright",
       legend = c(paste("Skewness:", round(cssml_skew, 3)),
                  paste("Kurtosis:", round(cssml_kurt, 3))),
       bty = "n", cex = 0.9)

# 3. Q-Q plot
qqnorm(cssml_res_clean, main = "CSS-ML: Normal Q-Q Plot",
       col = "#E41A1C", pch = 20,
       cex.main = 1.3, cex.lab = 1.1)
qqline(cssml_res_clean, col = "black", lwd = 2)
grid(col = "gray90")

# 4. ACF
acf(cssml_res_clean, main = "CSS-ML: ACF of Residuals",
    lag.max = 40, col = "#E41A1C", lwd = 2,
    cex.main = 1.3, cex.lab = 1.1)

dev.off()
cat("✓\n")

# ==================== DIAGNOSTIC PLOT: PMM2 ====================
cat("Creating PMM2 diagnostics... ")

# Extract PMM2 residuals
pmm2_res <- pmm2_fit@residuals
pmm2_res_clean <- pmm2_res[is.finite(pmm2_res)]

png(file.path(plots_dir, "12_pmm2_diagnostics.png"),
    width = 12, height = 10, units = "in", res = 300)

par(mfrow = c(2, 2), mar = c(4, 4, 3, 2), bg = "white")

# 1. Residuals over time
plot(pmm2_res_clean, type = "l", col = "#377EB8", lwd = 1.2,
     main = "PMM2: Residuals Over Time",
     xlab = "Observation Index", ylab = "Residuals",
     cex.main = 1.3, cex.lab = 1.1)
abline(h = 0, col = "black", lty = 2, lwd = 1.5)
grid(col = "gray90")

# 2. Histogram with normal overlay
hist(pmm2_res_clean, breaks = 50, col = "#377EB880", border = "white",
     main = "PMM2: Histogram of Residuals",
     xlab = "Residuals", freq = FALSE,
     cex.main = 1.3, cex.lab = 1.1)
curve(dnorm(x, mean = mean(pmm2_res_clean), sd = sd(pmm2_res_clean)),
      add = TRUE, col = "black", lwd = 2)
# Add skewness and kurtosis
pmm2_skew <- arima111_results[arima111_results$Method == "PMM2", "Skewness"]
pmm2_kurt <- arima111_results[arima111_results$Method == "PMM2", "Kurtosis"]
legend("topright",
       legend = c(paste("Skewness:", round(pmm2_skew, 3)),
                  paste("Kurtosis:", round(pmm2_kurt, 3))),
       bty = "n", cex = 0.9)

# 3. Q-Q plot
qqnorm(pmm2_res_clean, main = "PMM2: Normal Q-Q Plot",
       col = "#377EB8", pch = 20,
       cex.main = 1.3, cex.lab = 1.1)
qqline(pmm2_res_clean, col = "black", lwd = 2)
grid(col = "gray90")

# 4. ACF
acf(pmm2_res_clean, main = "PMM2: ACF of Residuals",
    lag.max = 40, col = "#377EB8", lwd = 2,
    cex.main = 1.3, cex.lab = 1.1)

dev.off()
cat("✓\n")

# ==================== COMPARATIVE DIAGNOSTIC PLOT ====================
cat("Creating comparative diagnostics... ")

png(file.path(plots_dir, "13_comparative_diagnostics.png"),
    width = 14, height = 8, units = "in", res = 300)

par(mfrow = c(2, 4), mar = c(4, 4, 3, 2), bg = "white")

# CSS-ML panels
# 1. CSS-ML Residuals
plot(cssml_res_clean, type = "l", col = "#E41A1C", lwd = 1.2,
     main = "CSS-ML: Residuals", xlab = "Time", ylab = "Residuals",
     cex.main = 1.2, cex.lab = 1.0)
abline(h = 0, col = "black", lty = 2)

# 2. CSS-ML Histogram
hist(cssml_res_clean, breaks = 40, col = "#E41A1C80", border = "white",
     main = "CSS-ML: Histogram", xlab = "Residuals", freq = FALSE,
     cex.main = 1.2, cex.lab = 1.0)
curve(dnorm(x, mean = mean(cssml_res_clean), sd = sd(cssml_res_clean)),
      add = TRUE, col = "black", lwd = 2)

# 3. CSS-ML Q-Q
qqnorm(cssml_res_clean, main = "CSS-ML: Q-Q Plot", col = "#E41A1C", pch = 20,
       cex.main = 1.2, cex.lab = 1.0)
qqline(cssml_res_clean, col = "black", lwd = 2)

# 4. CSS-ML ACF
acf(cssml_res_clean, main = "CSS-ML: ACF", lag.max = 30, col = "#E41A1C",
    cex.main = 1.2, cex.lab = 1.0)

# PMM2 panels
# 5. PMM2 Residuals
plot(pmm2_res_clean, type = "l", col = "#377EB8", lwd = 1.2,
     main = "PMM2: Residuals", xlab = "Time", ylab = "Residuals",
     cex.main = 1.2, cex.lab = 1.0)
abline(h = 0, col = "black", lty = 2)

# 6. PMM2 Histogram
hist(pmm2_res_clean, breaks = 40, col = "#377EB880", border = "white",
     main = "PMM2: Histogram", xlab = "Residuals", freq = FALSE,
     cex.main = 1.2, cex.lab = 1.0)
curve(dnorm(x, mean = mean(pmm2_res_clean), sd = sd(pmm2_res_clean)),
      add = TRUE, col = "black", lwd = 2)

# 7. PMM2 Q-Q
qqnorm(pmm2_res_clean, main = "PMM2: Q-Q Plot", col = "#377EB8", pch = 20,
       cex.main = 1.2, cex.lab = 1.0)
qqline(pmm2_res_clean, col = "black", lwd = 2)

# 8. PMM2 ACF
acf(pmm2_res_clean, main = "PMM2: ACF", lag.max = 30, col = "#377EB8",
    cex.main = 1.2, cex.lab = 1.0)

dev.off()
cat("✓\n")

# ==================== SUMMARY ====================
cat("\n✓ All WTI diagnostic plots created successfully!\n")
cat("\nGenerated files:\n")
cat("  - 11_cssml_diagnostics.png (CSS-ML method)\n")
cat("  - 12_pmm2_diagnostics.png (PMM2 method)\n")
cat("  - 13_comparative_diagnostics.png (Side-by-side comparison)\n")
cat("\nLocation:", file.path(plots_dir), "\n")

# Print diagnostic summary
cat("\n=== Diagnostic Summary ===\n")
cat("CSS-ML:\n")
cat("  Skewness:", round(cssml_skew, 3), "\n")
cat("  Kurtosis:", round(cssml_kurt, 3), "\n")
cat("  AIC:", arima111_results[arima111_results$Method == "CSS-ML", "AIC"], "\n")
cat("  BIC:", arima111_results[arima111_results$Method == "CSS-ML", "BIC"], "\n")

cat("\nPMM2:\n")
cat("  Skewness:", round(pmm2_skew, 3), "\n")
cat("  Kurtosis:", round(pmm2_kurt, 3), "\n")
cat("  AIC:", arima111_results[arima111_results$Method == "PMM2", "AIC"], "\n")
cat("  BIC:", arima111_results[arima111_results$Method == "PMM2", "BIC"], "\n")
