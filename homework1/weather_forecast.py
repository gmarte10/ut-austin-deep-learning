from typing import Tuple

import torch


class WeatherForecast:
    def __init__(self, data_raw: list[list[float]]):
        """
        You are given a list of 10 weather measurements per day.
        Save the data as a PyTorch (num_days, 10) tensor,
        where the first dimension represents the day,
        and the second dimension represents the measurements.
        """
        
        self.data = torch.as_tensor(data_raw).view(-1, 10)

    def find_min_and_max_per_day(self) -> Tuple[torch.Tensor]:
        """
        Find the max and min temperatures per day

        Returns:
            min_per_day: tensor of size (num_days,)
            max_per_day: tensor of size (num_days,)
        """
        min_per_day = torch.min(self.data, dim=1)
        max_per_day = torch.max(self.data, dim=1)
        return (min_per_day.values, max_per_day.values)
    
    def find_the_largest_drop(self) -> torch.Tensor:
        """
        Find the largest change in day over day average temperature.
        This should be a negative number.

        Returns:
            tensor of a single value, the difference in temperature
        """
        avg_per_day = torch.mean(self.data, dim=1)
        changes = avg_per_day[1:] - avg_per_day[:-1]
        return torch.neg(torch.max(torch.abs(changes)))
    
    def find_the_most_extreme_day(self) -> torch.Tensor:
        """
        For each day, find the measurement that differs the most from the day's average temperature

        Returns:
            tensor with size (num_days,)
        """
        avg_per_day = torch.mean(self.data, dim=1)
        sd = self.data[None, ...]
        apd = avg_per_day[..., None]
        diff = torch.squeeze(torch.abs(sd - apd), 0)
        index = torch.max(diff, dim=1).indices
        row = torch.arange(self.data.shape[0])
        return self.data[row, index]
    
    def max_last_k_days(self, k: int) -> torch.Tensor:
        """
        Find the maximum temperature over the last k days

        Returns:
            tensor of size (k,)
        """
        rows = torch.neg(torch.as_tensor(k))
        k_days = self.data[rows:]
        max_temp = torch.max(k_days, dim=1)
        return max_temp.values

    def predict_temperature(self, k: int) -> torch.Tensor:
        """
        From the dataset, predict the temperature of the next day.
        The prediction will be the average of the temperatures over the past k days.

        Args:
            k: int, number of days to consider

        Returns:
            tensor of a single value, the predicted temperature
        """
        k = torch.neg(torch.as_tensor(k))
        k_days = self.data[k:]
        return torch.mean(k_days)

    def what_day_is_this_from(self, t: torch.FloatTensor) -> torch.LongTensor:
        """
        You go on a stroll next to the weather station, where this data was collected.
        You find a phone with severe water damage.
        The only thing that you can see in the screen are the
        temperature reading of one full day, right before it broke.

        You want to figure out what day it broke.

        The dataset we have starts from Monday.
        Given a list of 10 temperature measurements, find the day in a week
        that the temperature is most likely measured on.

        We measure the difference using 'sum of absolute difference
        per measurement':
            d = |x1-t1| + |x2-t2| + ... + |x10-t10|

        Args:
            t: tensor of size (10,), temperature measurements

        Returns:
            tensor of a single value, the index of the closest data element
        """
        d = torch.sum(torch.abs(self.data - t), dim=1)
        return torch.argmin(d)
    