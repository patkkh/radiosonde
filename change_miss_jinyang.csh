#!/bin/csh -f 

set stid = "47169"
setenv LANG  "UTF-8"
cd ../daou/RSG-20A/$stid
foreach files (`ls UPP*`)
echo $files
set fname = `echo $files | cut -d. -f1`
set output = $fname.sed
cat $files | sed 's/,/ NaN /g' > $output
end
