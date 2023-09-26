% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  PlotDepthinFeet
%  Sept. 22, 2023
%  M. E. Kress, Ph. D.
%  College of Staten Island, CUNY
% 
%   Plot CSI Sensor Data in Feet for comparison with SWMM.
%   This is a utility routine that reads a drop file containing the 
%   the data and window indicies for CSI Sensor data located in the current 
%   directory  whcih is stored in inches and plots the data in the window
%   in feet for comparison with  SWMM
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%   Clear and Read Drop File with the plotting information
%
clear
DropFile="CSI020423Run012223"
load(DropFile)
PlotUnits="Feet"
if(PlotUnits=="Feet")
    PlotDivisor=12.
else
    PlotDivsor=1.
end
figtt=figure
ax1 = subplot(1,1,1); % top subplot
plot(ax1,fData.dt(wdwin),fData.depth(wdwin)/PlotDivisor,'r','linewidth',1.5)
title(ax1,strcat(RunName," Date ",StartTime)); xlabel(ax1,'Observation Date');
ylabel(ax1,' Water Depth Feet ');
PlotSave2(RunName,'DepthFt','Line',StartTime,figtt)
%
%   Write csv file of depth data and time.
%
WriteOutFile(RunName,'DepthFt','Line',StartTime,fData,wdwin)
%  
%   Save dropfile
%
save(strcat(RunName,"RunFt",datestr(StartDate,'mmddyy'),".mat"))
%
%   Subroutine for output
%
function WriteOutFile(RunName,VariableName,ptype,StartDate,fData,wdwin)
%   do interpolation here
%
    OutFileName=strcat(RunName,VariableName,ptype,datestr(StartDate,'mmddyy'),'.csv');  
    writetable(fData(wdwin,:),OutFileName)   
end   % End WriteOutFile