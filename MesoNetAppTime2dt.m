%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%   Covert MesoNet time data to the format used with FloodNet
%   Sample input time: {'20220728T000000-0400'}
%   January 9, 2023
%   M. E. Kress, Ph. D,
%    
%  example: MesoNet App input {'20220728T000000-0400'}
%           output Matlab datetime format 2022/07/28 00:00:00
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [dt] = MesoNetAppTime2dt(utcstring) 
    %   For utcstring in MesoNet App time format
    ttime=extractBefore(utcstring(:,1),'-');
    ttime=extractAfter(ttime(:,1),'T');    
    dt=datetime(strcat(extractBefore(utcstring(:,1),'T'),ttime), ...
        'InputFormat','yyyyMMddHHmmss','Format','yyyy/MM/dd HH:mm:ss');
    dt.TimeZone='America/New_York';
end


