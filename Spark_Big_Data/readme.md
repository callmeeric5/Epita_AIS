## Final Assignment


## Assignements questions : 

1. **Trip Analysis**: 

   - Average duration and distance of rides: Compare these metrics by time of day, day of week, and month of year. This can reveal patterns such as longer trips during rush hours, on weekends, or during holiday seasons.
     
     check .ipynb or GCP for details

   - Popular locations: Identify the top 10 pickup and dropoff locations. This could be interesting when mapped visually.

check .ipynb or GCP for details

2. **Tip Analysis**:

   - Tip percentage by trip: Do some locations tip more than others? Is there a correlation between distance and tip? 
   
    Yes, people are willing to tip more in some locations but there is no strong correlation between distance and tip, check .ipynb or GCP for details

   - Tips by time: Does the time of day, week, or even year affect tipping behavior? You could cross-reference this with holidays or events.
     
  No, there is no relevant result to prove it.
     
     
   - Does the payment type affect the tipping

Yes, the most popluar one the pay_type: 1 but there are some nagative values exsist, I assume it is caused by the coupon or other promotion events.

3. **Fare Analysis**:

  - Can you calculate the average fare by pull & drop location ?

    check .ipynb or GCP for details
    
  - Can you calculate the average fare by Passenger count ? to see if there is any correlation with passenger count and fare amount

    check .ipynb or GCP for details
    
  - Can you correlate the fare amount and the distance trip ? 

   check .ipynb or GCP for details

4. **Traffic Analysis**:

   - Trip speed: Create a new feature for the average speed of a trip, and use this to infer traffic conditions by trying to find if for similar trip (when they exist) they more or less have the same avg speed or not, try then to group the avg speed by trip then hour, day, week

For the similiar trip, the avg speed is similar

5. **Demand Prediction**:

  - Feature engineering: Use the date and time of the pickups to create features for the model, such as hour of the day, day of the week, etc.

   check .ipynb or GCP for details

  - Regression model: Use a regression model (such as linear regression) to predict the number of pickups in the next hour based on the features.

    check .ipynb or GCP for details
