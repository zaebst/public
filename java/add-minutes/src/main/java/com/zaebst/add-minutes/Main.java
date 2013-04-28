package com.zaebst.AddMinutes;

class AddMinutesMain {
   public static void main(String argv[]) {
      AddMinutes adm = new AddMinutes();
      String blah = adm.AddMinutes("11:55 PM", 15);
      System.out.println(blah); 
   }
}

