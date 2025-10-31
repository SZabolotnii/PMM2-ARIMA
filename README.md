# PMM2-ARIMA: Застосування Методу Максимізації Поліномів для ARIMA Моделей

[English version below](#english-version)

## Про проект

Цей репозиторій містить повну дослідницьку платформу для порівняння методу максимізації поліномів другого порядку (PMM2) з класичними методами оцінювання параметрів ARIMA моделей. Проект включає теоретичне обґрунтування, Monte Carlo симуляції, емпіричний аналіз та LaTeX-рукопис наукової статті.

**Автор:** Сергій Заболотній
**Афіліація:** Черкаський державний бізнес-коледж
**Email:** zabolotnii.serhii@csbc.edu.ua

## Основні результати

PMM2 демонструє значні переваги для часових рядів з негаусовими інноваціями:

- **Ефективність для асиметричних розподілів**: RE = 1.58-1.90 (37-47% зменшення MSE)
- **Робастність до важких хвостів**: Стабільна продуктивність для гамма, логнормального та χ² розподілів
- **Обчислювальна ефективність**: Часто швидше 1-2x порівняно з CSS-ML для простих моделей
- **Теоретична обґрунтованість**: RE ≈ 1.0 для гаусових інновацій (консистентність)

## Структура репозиторію

```
PMM2-ARIMA/
├── README.md                          # Цей файл
├── .gitignore                         # Git конфігурація
│
├── Experiment_R/                      # Основні експерименти на R
│   ├── comprehensive_study.R          # Комплексне порівняння моделей
│   ├── create_visualizations.R        # Генерація візуалізацій
│   ├── generate_report.R              # Створення аналітичного звіту
│   ├── run_full_study.R               # Головний скрипт (запускає всі етапи)
│   ├── create_wti_diagnostics.R       # Діагностика WTI даних
│   ├── arima_oil_quick_demo.R         # Швидка демонстрація
│   ├── data/                          # Дані (DCOILWTICO.csv)
│   ├── results/                       # Згенеровані результати
│   │   ├── full_results.csv           # Повні результати моделювання
│   │   ├── ANALYTICAL_REPORT.md       # Аналітичний звіт
│   │   └── plots/                     # Графіки (PNG, 300 DPI)
│   └── README.md                      # Детальна документація експериментів
│
├── PMM2_ARIMA_repro/                  # Пакет відтворюваності для рецензентів
│   ├── scripts/                       # Скрипти аналізу
│   │   ├── run_full_study.R           # WTI експеримент
│   │   ├── run_monte_carlo.R          # Monte Carlo симуляції
│   │   ├── comprehensive_study.R      # Підгонка моделей
│   │   ├── create_visualizations.R    # Візуалізації
│   │   └── generate_report.R          # Звіт
│   ├── data/                          # Вхідні дані
│   ├── results/                       # Результати та графіки
│   │   └── monte_carlo/               # Monte Carlo результати
│   ├── DESCRIPTION                    # R залежності
│   ├── Makefile                       # Автоматизація збірки
│   └── README.md                      # Інструкції для рецензентів
│
├── Experiment_Python/                 # Експериментальна Python імплементація
│   └── pmm2_arima_corrected.py        # PMM2 алгоритм на Python
│
├── LaTeX/                             # Рукопис статті
│   ├── PMM2_ARIMA.tex                 # Основний LaTeX файл
│   ├── PMM2_ARIMA.pdf                 # Зкомпільований PDF
│   ├── references.bib                 # Бібліографія
│   └── [артефакти збірки]             # .aux, .log, .out, тощо
│
└── data-search/                       # Документація пошуку даних
    └── [документи про джерела даних]
```

## Швидкий старт

### Передумови

**R пакети (обов'язкові):**
```r
install.packages(c(
  "ggplot2",        # Візуалізація
  "gridExtra",      # Багатопанельні графіки
  "RColorBrewer",   # Колірні палітри
  "tseries"         # Тест Дікі-Фуллера
))

# PMM2 імплементація
remotes::install_github("SZabolotnii/EstemPMM")
```

**Опційні залежності:**
```bash
# Для конвертації звіту у HTML/PDF
brew install pandoc              # macOS
sudo apt install pandoc          # Ubuntu/Debian

# Для компіляції LaTeX рукопису
brew install --cask mactex       # macOS
sudo apt install texlive-full    # Ubuntu/Debian
```

### Запуск повного дослідження

```r
# Опція 1: З директорії Experiment_R
setwd("PMM2-ARIMA/Experiment_R")
source("run_full_study.R")

# Опція 2: З кореневої директорії
source("Experiment_R/run_full_study.R")

# Опція 3: Використовуючи пакет відтворюваності
setwd("PMM2-ARIMA/PMM2_ARIMA_repro")
Rscript scripts/run_full_study.R
```

Очікуваний час виконання: **3-5 хвилин**

### Перегляд результатів

```r
# Відкрити аналітичний звіт
file.show("Experiment_R/results/ANALYTICAL_REPORT.md")

# Завантажити результати в R
results <- read.csv("Experiment_R/results/full_results.csv")
View(results)

# Переглянути графіки
list.files("Experiment_R/results/plots", pattern = "\\.png$")
```

## Використання

### Базовий приклад

```r
library(EstemPMM)

# Завантажити дані WTI (ціни на нафту)
wti <- read.csv("Experiment_R/data/DCOILWTICO.csv")
wti_clean <- na.omit(wti$DCOILWTICO)

# Підгонка ARIMA(1,1,0) обома методами
model_css <- arima(wti_clean, order = c(1, 1, 0), method = "CSS-ML")
model_pmm2 <- arima_pmm2(wti_clean, order = c(1, 1, 0))

# Порівняння
cat("AIC (CSS-ML):", AIC(model_css), "\n")
cat("AIC (PMM2):  ", model_pmm2$aic, "\n")
```

### Запуск Monte Carlo симуляцій

```bash
# Повний запуск (2000 повторень, ~20-40 хвилин)
cd PMM2_ARIMA_repro
Rscript scripts/run_monte_carlo.R

# Швидка перевірка (200 повторень)
Rscript scripts/run_monte_carlo.R --reps=200

# Кастомізація
Rscript scripts/run_monte_carlo.R \
  --reps=1000 \
  --seed=42 \
  --standardize-innov=true
```

### Генерація візуалізацій

```r
# З директорії Experiment_R (після запуску comprehensive_study.R)
source("create_visualizations.R")

# Результат: 10 графіків у results/plots/
# 01_aic_comparison.png
# 02_bic_comparison.png
# 03_rmse_comparison.png
# ... тощо
```

## Ключові скрипти

### `Experiment_R/comprehensive_study.R`
Головний скрипт моделювання:
- Завантажує WTI дані (FRED: DCOILWTICO)
- Підгоняє 6 ARIMA специфікацій: (0,1,1), (1,1,0), (1,1,1), (2,1,1), (1,1,2), (2,1,2)
- Порівнює CSS-ML vs PMM2
- Збирає метрики: AIC, BIC, RMSE, MAE, MAPE, асиметрія залишків, ексцес
- Зберігає результати у CSV та RDS форматах

### `Experiment_R/create_visualizations.R`
Створює 10 публікаційних графіків:
1. Порівняння AIC
2. Порівняння BIC
3. Порівняння RMSE
4. Час обчислень
5. Ексцес залишків
6. Асиметрія залишків
7. Тепловий графік продуктивності
8. Різниці методів
9. Діагностика найкращої моделі
10. Зведена статистика

### `Experiment_R/generate_report.R`
Генерує структурований Markdown звіт з:
- Резюме виконавчого рівня
- Характеристики даних
- Специфікації моделей
- Комплексні результати
- Порівняння методів
- Аналіз залишків
- Висновки та рекомендації

### `PMM2_ARIMA_repro/scripts/run_monte_carlo.R`
Відтворює Monte Carlo дослідження з статті:
- 4 розподіли інновацій (Гаус, Гамма, Логнормальний, χ²)
- 4 розміри вибірки (100, 200, 500, 1000)
- 2000 повторень на конфігурацію
- Обчислює RE, bias, variance, MSE
- Генерує таблиці для LaTeX рукопису

## Відтворюваність

Проект розроблений з акцентом на повну відтворюваність:

1. **Версійність пакетів**: `PMM2_ARIMA_repro/DESCRIPTION` фіксує всі R залежності
2. **Детермінізм**: Усі випадкові симуляції використовують `set.seed(12345)`
3. **Нумерація артефактів**: Графіки нумеруються для відповідності LaTeX підписам
4. **Автоматизація**: `Makefile` для однокомандного відтворення
5. **Документація**: Детальні README у кожній піддиректорії

### Відтворення рукопису

```bash
cd PMM2_ARIMA_repro

# 1. Згенерувати всі результати
make all

# 2. Зкомпілювати LaTeX
cd ../LaTeX
pdflatex PMM2_ARIMA.tex
bibtex PMM2_ARIMA
pdflatex PMM2_ARIMA.tex
pdflatex PMM2_ARIMA.tex

# Або використовуючи latexmk
latexmk -pdf PMM2_ARIMA.tex
```

## Результати

### WTI Case Study (N = 8,020 спостережень)

| Модель      | Метод  | AIC      | BIC      | RMSE  | Час (с) |
|-------------|--------|----------|----------|-------|---------|
| ARIMA(0,1,1)| CSS-ML | 7,245.32 | 7,258.45 | 9.12  | 0.082   |
| ARIMA(0,1,1)| PMM2   | 7,243.18 | 7,256.31 | 9.11  | 0.045   |
| ARIMA(1,1,0)| CSS-ML | 7,246.89 | 7,260.02 | 9.13  | 0.074   |
| ARIMA(1,1,0)| PMM2   | 7,244.52 | 7,257.65 | 9.12  | 0.039   |

PMM2 **перемагає або прирівнюється** за всіма метриками, будучи **швидшим у 1.5-2x**.

### Monte Carlo симуляції

#### ARIMA(1,1,0), N=500, Гамма(2,1) інновації

| Параметр | Метод  | Bias    | Variance | MSE    | RE    |
|----------|--------|---------|----------|--------|-------|
| φ₁       | CSS-ML | -0.0012 | 0.00198  | 0.00198| 1.00  |
| φ₁       | PMM2   | -0.0008 | 0.00125  | 0.00125| 1.58  |

**RE = 1.58** означає **37% покращення MSE** для PMM2.

#### Відносна ефективність (RE) vs Асиметрія

| Розподіл      | γ₃   | RE (N=500) |
|---------------|------|------------|
| Гаус          | 0.00 | 1.02       |
| Гамма(2,1)    | 1.41 | 1.58       |
| Логнормальний | 2.00 | 1.71       |
| χ²(3)         | 1.63 | 1.90       |

**Висновок**: Ефективність PMM2 **сильно корелює** з асиметрією розподілу.

## Компіляція LaTeX рукопису

```bash
cd LaTeX

# Опція 1: Використовуючи pdflatex
pdflatex PMM2_ARIMA.tex
bibtex PMM2_ARIMA
pdflatex PMM2_ARIMA.tex
pdflatex PMM2_ARIMA.tex

# Опція 2: Використовуючи latexmk (рекомендовано)
latexmk -pdf PMM2_ARIMA.tex

# Очистка артефактів
latexmk -c
```

**Рукопис включає:**
- Теоретичне обґрунтування PMM2 для ARIMA
- Повну специфікацію алгоритму
- Monte Carlo результати з 10+ таблицями
- WTI case study з 10 графіками
- Формальні теореми асимптотичної нормальності

## Цитування

Якщо ви використовуєте цей код або результати у вашому дослідженні, будь ласка, цитуйте:

```bibtex
@article{zabolotnii2025pmm2arima,
  title   = {Застосування Методу Максимізації Поліномів для Оцінювання Параметрів
             ARIMA Моделей з Асиметричними Негаусовими Інноваціями},
  author  = {Заболотній, Сергій},
  journal = {[Назва журналу]},
  year    = {2025},
  note    = {Manuscript in preparation}
}

@software{zabolotnii2025pmm2code,
  title   = {PMM2-ARIMA: Implementation and Reproducibility Package},
  author  = {Заболотній, Сергій},
  year    = {2025},
  url     = {https://github.com/SZabolotnii/PMM2-ARIMA}
}
```

## Ліцензія

Цей проект є частиною пакету `EstemPMM` та використовує ту саму ліцензію.

## Контакти

**Сергій Заболотній**
Черкаський державний бізнес-коледж
Email: zabolotnii.serhii@csbc.edu.ua
GitHub: [@SZabolotnii](https://github.com/SZabolotnii)

## Подяки

- **Проф. Ю.П. Кунченко** за розробку теорії методу максимізації поліномів
- **FRED (Federal Reserve Economic Data)** за надання WTI даних
- R спільноті за відкриті інструменти аналізу часових рядів

---

# English Version

## About

This repository contains a comprehensive research platform comparing the second-order Polynomial Maximization Method (PMM2) with classical ARIMA parameter estimation methods. The project includes theoretical foundations, Monte Carlo simulations, empirical analysis, and a LaTeX manuscript.

**Author:** Serhii Zabolotnii
**Affiliation:** Cherkasy State Business College
**Email:** zabolotnii.serhii@csbc.edu.ua

## Key Findings

PMM2 demonstrates significant advantages for time series with non-Gaussian innovations:

- **Efficiency for asymmetric distributions**: RE = 1.58-1.90 (37-47% MSE reduction)
- **Robustness to heavy tails**: Stable performance for Gamma, Lognormal, and χ² distributions
- **Computational efficiency**: Often 1.5-2x faster than CSS-ML for simple models
- **Theoretical soundness**: RE ≈ 1.0 for Gaussian innovations (consistency)

## Repository Structure

See the Ukrainian section above for detailed structure.

## Quick Start

### Prerequisites

**Required R packages:**
```r
install.packages(c(
  "ggplot2", "gridExtra", "RColorBrewer", "tseries"
))
remotes::install_github("SZabolotnii/EstemPMM")
```

### Run Full Study

```r
source("Experiment_R/run_full_study.R")
```

Expected runtime: **3-5 minutes**

### View Results

```r
file.show("Experiment_R/results/ANALYTICAL_REPORT.md")
results <- read.csv("Experiment_R/results/full_results.csv")
```

## Basic Example

```r
library(EstemPMM)

# Load WTI oil price data
wti <- read.csv("Experiment_R/data/DCOILWTICO.csv")
wti_clean <- na.omit(wti$DCOILWTICO)

# Fit ARIMA(1,1,0) with both methods
model_css <- arima(wti_clean, order = c(1, 1, 0), method = "CSS-ML")
model_pmm2 <- arima_pmm2(wti_clean, order = c(1, 1, 0))

# Compare
cat("AIC (CSS-ML):", AIC(model_css), "\n")
cat("AIC (PMM2):  ", model_pmm2$aic, "\n")
```

## Monte Carlo Simulations

```bash
cd PMM2_ARIMA_repro

# Full run (2000 replications, ~20-40 minutes)
Rscript scripts/run_monte_carlo.R

# Quick check (200 replications)
Rscript scripts/run_monte_carlo.R --reps=200
```

## Reproducibility

The project emphasizes full reproducibility:

1. **Package versioning**: `DESCRIPTION` locks all R dependencies
2. **Determinism**: All random simulations use `set.seed(12345)`
3. **Artifact numbering**: Plots numbered to match LaTeX captions
4. **Automation**: `Makefile` for one-command reproduction
5. **Documentation**: Detailed READMEs in each subdirectory

## Key Results

### WTI Case Study (N = 8,020 observations)

PMM2 **wins or ties** on all metrics while being **1.5-2x faster**.

### Monte Carlo Simulations

For ARIMA(1,1,0), N=500, Gamma(2,1) innovations: **RE = 1.58** (37% MSE improvement).

### Relative Efficiency vs Asymmetry

| Distribution  | γ₃   | RE (N=500) |
|---------------|------|------------|
| Gaussian      | 0.00 | 1.02       |
| Gamma(2,1)    | 1.41 | 1.58       |
| Lognormal     | 2.00 | 1.71       |
| χ²(3)         | 1.63 | 1.90       |

**Conclusion**: PMM2 efficiency **strongly correlates** with distribution asymmetry.

## LaTeX Compilation

```bash
cd LaTeX
latexmk -pdf PMM2_ARIMA.tex
```

## Citation

```bibtex
@article{zabolotnii2025pmm2arima,
  title   = {Application of Polynomial Maximization Method for Estimating
             ARIMA Models with Asymmetric Non-Gaussian Innovations},
  author  = {Zabolotnii, Serhii},
  year    = {2025},
  note    = {Manuscript in preparation}
}
```

## License

This project is part of the `EstemPMM` package and follows the same license.

## Contact

**Serhii Zabolotnii**
Cherkasy State Business College
Email: zabolotnii.serhii@csbc.edu.ua
GitHub: [@SZabolotnii](https://github.com/SZabolotnii)
