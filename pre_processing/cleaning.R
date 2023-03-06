library(dplyr)
library(readr)
library(stringr)

# Water level
wl_files <- list.files("./data/WL/raw/")

for (i in 1:length(wl_files)) {
  wl <- read_delim(
    paste0("./data/WL/raw/", wl_files[i]), delim = "\t", guess_max = Inf, 
    show_col_types = F)
  
  wl <- wl |>
    mutate(
      Date = as.Date(Date, format = "%Y/%m/%d")
    ) |>
    rename_all(tolower) |>
    rename(
      water_level = value 
    )

  write_rds(
    wl, paste0("./data/clean/WL/", str_remove(wl_files[i], ".csv$")), 
    compress = "gz")
}

# Met Eireann

fix_names <- function(file) {
  header <- read_lines(file, n_max = 1) |> 
    str_split_1(",")
  id <- which(stringr::str_detect(header, "^ind") == T)
  fixed_ind <- rep("ind", length(id)) |>
    paste0("_", header[id + 1])
  header[id] <- fixed_ind
  return(header)
}

me_files <- list.files("./data/ME/raw/")

for (i in 1:length(me_files)) {
  me <- read_delim(
    paste0("./data/ME/raw/", me_files[i]), delim = ",", na = " ", 
    guess_max = Inf) |>
    suppressMessages()
  names(me) <- fix_names(paste0("./data/ME/raw/", me_files[i]))
  me <- me |>
    mutate(
      date = as.Date(date, format = "%d-%b-%Y")
    )
  
  write_rds(
    me, paste0("./data/clean/ME/", str_remove(me_files[i], ".csv$")),
    compress = "gz")
}
