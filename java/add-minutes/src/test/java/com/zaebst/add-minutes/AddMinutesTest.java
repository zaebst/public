package com.zaebst.AddMinutes;

import junit.framework.TestCase;
import com.zaebst.AddMinutes.AddMinutes;



public class AddMinutesTest extends TestCase {
   public void test_pm_to_am() {
      AddMinutes adm = new AddMinutes();
      String found = adm.AddMinutes("11:55 PM", 15);
      String expected = "12:10 AM";
      assertEquals(found, expected);
   }
   public void test_am_to_pm() {
      AddMinutes adm = new AddMinutes();
      String found = adm.AddMinutes("11:55 AM", 15);
      String expected = "12:10 PM";
      assertEquals(found, expected);
   }
   public void test_pm_to_pm() {
      AddMinutes adm = new AddMinutes();
      String found = adm.AddMinutes("11:55 PM", 1440); /* 1440 minutes in a day */
      String expected = "11:55 PM";
      assertEquals(found, expected);
   }
   /* 
      Here it is worth looking into Junit >= 4.0 which has tests for exceptions.  Then we could test for the IllegalArgumentException.  
   */
}
