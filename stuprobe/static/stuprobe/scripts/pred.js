function graph(history) {
    count = 1;
    history_sum = 0;
    percent_attendance = [];
    days = [];
    labels = [];


    for(i=1; i<50; i++) {
      labels.push(i);
    }

    

    
    for(i=0; i<history.length; i++) {
        
        if (history[i] == 1){
            history_sum++;
        }
        percent_attendance.push((history_sum/count)*100);
        
        days.push(count);
        count++;

    }
    console.log(days);
    console.log(percent_attendance);




     //---------------used vars-----------------------
     var independent_variable = days;
     var dependent_variable = percent_attendance;
     var mean_x = 0 , mean_y = 0;


     var x_xb = [];
     var y_yb = [];
     var summation__x_xby_yb = 0;
     var summation__x_xb2 = 0;
     var summation__y_yb2 = 0;

     var r = 0;
     var Sy = 0;
     var Sx = 0;

     var b = 0;
     var a = 0;

     var min = 500, max = 600;

     var pred = [];
     var lper =0, pper = 0;


     var linefit = [];
     var color;
    //-------------------------------------------------






    //------populate with random data------------------
     // for (var i = 0; i < 10; i++) {
     //  dependent_variable.push(Math.floor(Math.random() * (max - min + 1) + min)); //y = close pe jo price hai
     
     //   independent_variable.push(i+1+2);//daily, monthly jo b assumption
     // }
     //------------------------------------------------   
      





     //---------------functions-------------------------
     function mulArray(a, b) {
         var c = [];
         for (var i = 0; i < Math.max(a.length, b.length); i++) {
           c.push((a[i] || 0) * (b[i] || 0));
         }
         return c;
     }
     function summation(arr){
       let retr = 0;
       arr.forEach(function(x){retr = retr + x;});
       return retr;
     }
     //-----------------------------------------------------------





     //-------mean-------------------------------------------
     sum_x = summation(independent_variable); 
     sum_y = summation(dependent_variable);

     mean_x = sum_x/independent_variable.length;
     mean_y = sum_y/dependent_variable.length;
     
     //-----------------------------------------------------------





     //-------differences----multiplications-----

     independent_variable.forEach(function(x){ x_xb.push(x - mean_x); }); //x - xb loaded
     dependent_variable.forEach(function(y){ y_yb.push(y - mean_y); }); //y - yb loaded
     //-----------------------------------------------------------

     
     console.log(y_yb)//zeros on same values




     //-------summations----------------

     summation__x_xby_yb = summation(mulArray(x_xb,y_yb));
     summation__x_xb2 = summation(mulArray(x_xb,x_xb));
     summation__y_yb2 = summation(mulArray(y_yb,y_yb));
     //-----------------------------------------------------------

     console.log("-----")
     console.log(summation__x_xby_yb)
     console.log(summation__x_xb2)
     console.log(summation__y_yb2)
     console.log("-----")




     //----------Calculation of slope---------------
     //b = r * (Sy/Sx)
     r = (summation__x_xby_yb/Math.sqrt(summation__x_xb2*summation__y_yb2));

     Sy = Math.sqrt(summation__y_yb2/dependent_variable.length);
     Sx = Math.sqrt(summation__x_xb2/independent_variable.length);

     b = r*(Sy/Sx);
     //-----------------------------------------------------------



    


     //----------Calculation of intercept-----------------
     a = mean_y - (b*mean_x);
     //-----------------------------------------------------------


     console.log(r,Sy,Sx,b,a);



     //-------prediction-------------------------------------
     for (var i = 0; i < 29; i++) {
       pred.push(NaN);
     }
     
     //-----------------------------------------------------------

     
     if (summation__x_xby_yb == 0 && summation__y_yb2 == 0) {
      pred.push(dependent_variable[0]);
      console.log("pred",pred);
       for(var i =0; i< 30;i++){
         linefit.push(dependent_variable[0]);
       }
     }
     else{
       if((b*(30)+a)>100){
        color = 'green';
        pred.push(100);
       }
        else{
          if((b*(30)+a)>=75 && (b*(30)+a)<=100){
            color = 'green';
            pred.push(b*(30)+a);
          }
          else {
            if((b*(30)+a)<=75 && (b*(30)+a)>0) {
              color = 'red';
              pred.push((b*(30)+a));
            }
            else {
              color = 'red';
              pred.push(0);
            }
          }
        }
        
      console.log("pred",pred);
       for(var i =0; i< 30;i++){
        y = b*[i]+a;
        linefit.push(y);
       }
     }
     console.log(linefit);
     

     //-------Graph--------------------------------------------------------
     var ctx = document.getElementById('chart').getContext('2d');
     var chart = new Chart(ctx, {
         // The type of chart we want to create
         type: 'line',
        // The data for our dataset
         data: {
            
             datasets: [{
                 label: 'Attendance',
                 fill: false,
                 backgroundColor: 'rgb(0,0,0)',
                 borderColor: 'rgb(0,0,0)',
                 
                 data: dependent_variable
             }
             ,{
                 label: 'Detention',
                 fill: false,
                 backgroundColor: color,
                 borderColor: color,
                 data: pred,
                 type: 'bubble',
                 radius: 5
             }
          ,{
               label: 'Fitted Curve',
               fill: false,
               backgroundColor: 'rgb(12, 92, 132)',
               borderColor: 'rgb(12, 92, 132)',
               data: linefit,
               type: 'line',
               borderWidth: 1,
               hidden: true
               
           }
        ],
             labels: labels
         },
     
         // Configuration options go here
         options: {
           scales: {
             yAxes: [{
                     display: true,
                     ticks: {
                         min : 0,
                         steps: 10,
                         stepValue: 5,
                         max: 100
                     }
                 }]
         }
         }
     });
     //--------------------------------------------------------------------------------

    if(color == 'green'){
      document.getElementById("msg").innerHTML = "No detention expected. :)";
      document.getElementById("msg").style.color = 'green';   
       
    }
    else if(color == 'red'){
      document.getElementById("msg").innerHTML = "Possible Detention    :(";
      document.getElementById("msg").style.color = 'red';  
    }


    
    
}