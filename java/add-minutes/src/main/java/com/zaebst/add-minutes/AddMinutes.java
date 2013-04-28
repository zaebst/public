package com.zaebst.AddMinutes;

public class AddMinutes {
  public String AddMinutes(String formatted_date, int minutes_to_add) throws IllegalArgumentException {
    int hours = 0;
    int minutes = 0;
    int seconds = 0;      /* used internally to represent the time */
    String am_or_pm = "";
    String formatted_date_plus_minutes = "";

    /* Expecting {h}h:mm {AM|PM} */

    String[] tokens = formatted_date.split(":| ");   /* Split the input on space and : charachters */

    /* If the number is not parseable by parseInt, then it will throw NumberFormatException e 

       In this case, we just let it fail.  Someone is trying to use the API in the wrong way.
       There is some debatable value in thowing a more useful error such as:
          throw new IllegalArgumentException("Encountered non-numeric hour or minute specification.  Please use time format {H}H:MM {AM|PM}");
    */

    try {
        hours = Integer.parseInt(tokens[0]);
        minutes = Integer.parseInt(tokens[1]);
    }
    catch ( NumberFormatException e )
    {
        throw new IllegalArgumentException("Encountered non-numeric hour or minute specification.  Please use time format {H}H:MM {AM|PM}");
    }

    if ( !tokens[2].equals("AM") && !tokens[2].equals("PM") ) {
        throw new IllegalArgumentException("Please specify AM or PM in time format {H}H:MM {AM|PM}");
    }
    else {
        am_or_pm = tokens[2];
    }

    /*  In most cases with time, you really want to find something stable, like localtime, which is based on epoch-seconds.  Then you can use a lot of the C libraries designed to deal with date conversion.
        Here we only need to worry about a 24 hour period.  There are still edge cases... do we allow someone to go past the end of the day and wrap to the next day?  I suppose so.
        seconds in a day: 86400
        seconds in a hour: 3600
        seconds in a minute: 60
        seconds in half-day: 43200
    */
    if ( am_or_pm.equals("PM") ) { seconds += 43200; } 
    seconds += 3600 * hours;
    seconds += 60   * minutes;
    seconds += 60   * minutes_to_add;

    while ( seconds > 86400 ) { seconds -= 86400; }               /* Get rid of any days */
    if ( seconds > 43200 ) { am_or_pm = "PM"; seconds -= 43200; }
    else { am_or_pm = "AM"; }

    hours = (int) seconds/3600; /* cast to int is similar to floor.  We want whole hours */
    seconds -= 3600 * hours;
    minutes = (int) seconds/60;
    seconds -= 60 * minutes;

    /* 12pm is followed by 1pm.  We represent 12 am or pm by zero internally, then convert it to 12. */
    if ( hours == 0 ) { hours = 12; }  

    formatted_date_plus_minutes = Integer.toString(hours) + ":" + Integer.toString(minutes) + " " + am_or_pm;

    return formatted_date_plus_minutes;
  }
} 
