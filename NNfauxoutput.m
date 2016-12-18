% Code for Sample Neural Network Output

%This variable determines the length of the fake mediation session. It is
%based on the Neural Network using 3 second epocs. Therefor there will be
%an entry in the fake ouput for every three seconds. This tool will not
%work if t1 is not divisable by 3 or at least 15 seconds long.
t1=120;

%Determining how many samples there would be
samples=[1:(t1/3)];

%Preallocating the output matrix
output=zeros(samples(end),3);

%Replazing the first column with time in seconds
output(:,1)=samples*3;

%Fake on trigger at 6 seconds
output(2,3)=1;

%Fake off trigger 6 seconds before end of sessions
output(samples(end)-2,2)=1;

%Peak medlevel score
peak=10.1;

%Meditation Level or score basically ( The 1-10 scale we talked about)
medlev=(peak*sin((pi/2).*(samples./samples(end))));

%Replacing Column Three with Medlevel
output(:,3)=medlev;

%Checking output
display(output)

%Write output to CSV file in Script Folder
csvwrite('NNouput_1',output)