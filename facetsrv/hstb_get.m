function [bact, tact] = hstb_get(lgps, time, type)

lgps = model_nameConvert(lgps, 'SLC');

tstart = datevec(time) - [0, 0, 0, 1.5, 0, 0];
tend = datevec(time) + [0, 0, 0, 1.5, 0, 0];

tstart_str = datestr(datenum(tstart), 'mm/dd/yyyy HH:MM:SS');
tend_str = datestr(datenum(tend), 'mm/dd/yyyy HH:MM:SS');

query = strcat(lgps, '//', type, '.HIST');

aidainit;
da = DaObject();
dr = DaReference(query, da);
dr.setParam('STARTTIME', tstart_str);
dr.setParam('ENDTIME', tend_str);
data = dr.getDaValue();

vals = data.get(0).getAsDoubles();
timestrings = char(data.get(1).getAsStrings());
times = datenum(timestrings);

tact = times(1);
bact = vals(1);

