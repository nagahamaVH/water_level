library(dplyr)
library(readr)

start_date <- as.Date("2022/06/01")
time_window <- 100

me_stations <- read_csv("./data/ME_StationDetails.csv", na = "(null)")
me_files <- list.files("./data/clean/ME")

# Selecting Clare stations
station_id <- me_stations |>
  filter(county == "Clare" & is.na(`close year`)) |>
  pull(`station name`)

id <- stringr::str_detect(
  me_files, pattern = paste0(station_id, collapse = "|"))

me_files_sample <- me_files[id]

# Concatenate data
me <- tibble()
for (i in 1:length(me_files_sample)) {
  me_i <- read_rds(paste0("./data/clean/ME/", me_files_sample[i]))
  me_i <- me_i |>
    filter(date > start_date & date <= start_date + time_window) |>
    mutate(
      station = stringr::str_extract(me_files_sample[i], "[[:digit:]]+") |>
        as.numeric()
    ) |>
    select(date, rain, station)
  me <- me |>
    bind_rows(me_i)
}

me <- me_stations |>
  select(`station name`, county, name, latitude, longitude) |>
  left_join(x = me, by = c("station" = "station name"))

# wl_stations <- read_csv("./data/ME_StationDetails.csv", na = "(null)")

write_rds(me, "./data/clare", compress = "gz")
