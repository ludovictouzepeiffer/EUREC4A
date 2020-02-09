;*********************************************************************************
;*********************************************************************************
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"
;*********************************************************************************

begin

;dayStr="24"

  MisVal = -999.
  MisVal@_FillValue = MisVal

;--- Read in DSHIP data (Weather Station)
print(" ")
print("Read in data")
 
 flnm = monStr+dayStr+"_min.dat"
 strs = asciiread(flnm,-1,"string")
 strs = str_sub_str(strs, "", "MisVal")
 nrow = numAsciiRow(flnm)

 nh  = 24
 nm  = 60
; ntim = 1440
 nhead = 3
; nrow = dimsizes(strs)
; nhead = nrows-ntim
 ntim = nrow - nhead
 nh = ntim/nm

 delim = "	"
 ncol = str_fields_count(strs(0), delim)

 print(ncol+"   "+nrow+"   "+nhead)
 print(strs(0))

 time = fspan(0,nh-0.01,ntim)

 fld = str_get_field(strs, 9, delim)
 var1D = stringtofloat(fld(nhead::))
 var1D@_FillValue=MisVal
 ta = where((var1D.gt.0).and.(var1D.lt.40),var1D,MisVal)
 ta@_FillValue=MisVal

 fld = str_get_field(strs, 10, delim)
 var1D = stringtofloat(fld(nhead::))
 var1D@_FillValue=MisVal
 ts = where((var1D.gt.15).and.(var1D.lt.35),var1D,MisVal)
 ts@_FillValue=MisVal

 fld = str_get_field(strs, 12, delim)
 var1D = stringtofloat(fld(nhead::))
 var1D@_FillValue=MisVal
 rh = where((var1D.gt.40).and.(var1D.lt.100),var1D,MisVal)
 rh@_FillValue=MisVal

 fld = str_get_field(strs, 14, delim)
 var1D = stringtofloat(fld(nhead::))
 var1D@_FillValue=MisVal
 wspd = where((var1D.gt.0).and.(var1D.lt.30),var1D,MisVal)
 wspd@_FillValue=MisVal

 fld = str_get_field(strs, 11, delim)
 var1D = stringtofloat(fld(nhead::))
 var1D@_FillValue=MisVal
 wdir = var1D

 fld = str_get_field(strs, 17, delim)
 var1D = stringtofloat(fld(nhead::))
 var1D@_FillValue=MisVal
 lat = where((var1D.gt.10).and.(var1D.lt.20),var1D,MisVal)
 lat@_FillValue=MisVal

 fld = str_get_field(strs, 18, delim)
 var1D = stringtofloat(fld(nhead::))
 var1D@_FillValue=MisVal
 lon = where((var1D.gt.-62).and.(var1D.lt.-52),var1D,MisVal)
 lon@_FillValue=MisVal

 ;--- calcul du LCL ---
 cp=1005.
 gr=9.81
 z0=29.
 taK=ta+273.15
 tlcl = 1/((1/(taK-55)) - (log(rh/100)/2840.)) + 55.
 zlcl = z0 - (cp*((tlcl-taK)/gr))

; print("  lat      lon        ts      ta       rh      wspd     wdir    LCL")
; print(sprintf("%6.2f", lat)+"   "+sprintf("%6.2f", lon)+"   "+sprintf("%6.2f", ts)+"   "+sprintf("%6.2f", ta)+"   "+sprintf("%6.2f", rh)+"   "+sprintf("%6.2f", wspd)+"   "+sprintf("%6.2f", wdir)+"   "+sprintf("%6.2f", zlcl))

nvar=8
data1D = new((/nvar,ntim/),float)
data1D(0,:)=lat
data1D(1,:)=lon
data1D(2,:)=ts
data1D(3,:)=ta
data1D(4,:)=rh
data1D(5,:)=wspd
data1D(6,:)=wdir
data1D(7,:)=zlcl
data1D@_FillValue=MisVal

;===================================
;--- Plot data (Weather Station)
;===================================

print(" ")
print("Plot data")

  ypts = (/ -10000., 10000./)
  xpts1 = (/10.,10./)
  xpts2 = (/22.,22./)


 MyColors  = (/"white","black","navyblue","Steelblue","PowderBlue","forestgreen","Palegreen","Gold","Orange","Red"/)

 wks   = gsn_open_wks("png","meteor_"+mon+dayStr)

 np=8
 plot0    = new((/np/),graphic)
 poly1    = new((/np/),graphic)
 poly2    = new((/np/),graphic)

;---Set plotting parameters

 res             = True
 res@gsnDraw     = False
 res@gsnFrame    = False

 res@vpWidthF    = 0.8
 res@vpHeightF   = 0.2

 res@tiMainFontHeightF       = 0.025

 res@xyMarkLineMode = "Lines"
 res@xyLineThicknessF = 3
 res@xyDashPattern    = 0

 res@gsnYRefLine            = 0

 res@trXMinF             = 0.
 res@trXMaxF             = 23.

; resources for "left" variable
  resL                        = res
  resR                        = res

; polyline
  resl                   = True 
  resl@gsLineThicknessF  = 2.
  resl@gsLineDashPattern = 2
  resl@gsLineColor      = "grey20"

;==============================
;==============================

print("panel 1: Lat/Lon")
ip=0

  dataL = data1D(0,:)
  dataR = data1D(1,:)

  resL@tiYAxisString     = "Latitude (~S~o~N~) [blue]"
  resL@trYMinF           =  min(dataL)-0.005*abs(min(dataL))
  resL@trYMaxF           =  max(dataL)+0.005*abs(max(dataL))
  resL@xyLineColors      = "steelblue"

  resR@tiYAxisString     = "Longitude (~S~o~N~) [green]"
  resR@trYMinF           =  min(dataR)-0.005*abs(min(dataR))
  resR@trYMaxF           =  max(dataR)+0.005*abs(max(dataR))
  resR@xyLineColors      = "forestgreen"
  
  plot0(ip) = gsn_csm_xy2(wks,time,dataL,dataR,resL,resR)

  delete(dataL)
  delete(dataR)

  poly1(ip) = gsn_add_polyline(wks,plot0(ip),xpts1,ypts,resl) 
  poly2(ip) = gsn_add_polyline(wks,plot0(ip),xpts2,ypts,resl) 

;----

print("panel 2: Temperatures")
ip=1

  dataL = data1D(2,:)
  dataR = data1D(3,:)

  resL@tiYAxisString     = "SST (~S~o~N~) [blue]"
  resL@trYMinF           =  min(dataL)-0.005*abs(min(dataL))
  resL@trYMaxF           =  max(dataL)+0.005*abs(max(dataL))
  resL@xyLineColors      = "steelblue"

  resR@tiYAxisString     = "T air (~S~o~N~) [green]"
  resR@trYMinF           =  min(dataR)-0.005*abs(min(dataR))
  resR@trYMaxF           =  max(dataR)+0.005*abs(max(dataR))
  resR@xyLineColors      = "forestgreen"
  
  plot0(ip) = gsn_csm_xy2(wks,time,dataL,dataR,resL,resR)

  delete(dataL)
  delete(dataR)

  poly1(ip) = gsn_add_polyline(wks,plot0(ip),xpts1,ypts,resl) 
  poly2(ip) = gsn_add_polyline(wks,plot0(ip),xpts2,ypts,resl) 

;==============================

print("panel 5")
ip=2

 data = data1D(4,:)

 res@trYMinF             = min(data)-0.05*abs(min(data))
 res@trYMaxF             = max(data)+0.05*abs(max(data))
 res@tiMainString        = " "
 res@tiYAxisString       = "RH (%)"
 res@tiXAxisString       = " "

 res@xyLineColor = MyColors(3)  
 plot0(ip)  = gsn_csm_xy (wks,time,data,res)
 delete(data)

  poly1(ip) = gsn_add_polyline(wks,plot0(ip),xpts1,ypts,resl) 
  poly2(ip) = gsn_add_polyline(wks,plot0(ip),xpts2,ypts,resl) 

;==============================

print("panel 6")
ip=3

 data = data1D(5,:)

 res@trYMinF             = min(data)-0.05*abs(min(data))
 res@trYMaxF             = max(data)+0.05*abs(max(data))
 res@tiMainString        = " "
 res@tiYAxisString       = "Wind speed (m/s)"
 res@tiXAxisString       = " "

 res@xyLineColor = MyColors(3)  
 plot0(ip)  = gsn_csm_xy (wks,time,data,res)
 delete(data)

  poly1(ip) = gsn_add_polyline(wks,plot0(ip),xpts1,ypts,resl) 
  poly2(ip) = gsn_add_polyline(wks,plot0(ip),xpts2,ypts,resl) 

;==============================

print("panel 7")
ip=4

 data = data1D(6,:)

 res@trYMinF             = min(data)-0.05*abs(min(data))
 res@trYMaxF             = max(data)+0.05*abs(max(data))
 res@tiMainString        = " "
 res@tiYAxisString       = "Wind direction (~S~o~N~)"
 res@tiXAxisString       = " "

 res@xyLineColor = MyColors(3)  
 plot0(ip)  = gsn_csm_xy (wks,time,data,res)
 delete(data)

  poly1(ip) = gsn_add_polyline(wks,plot0(ip),xpts1,ypts,resl) 
  poly2(ip) = gsn_add_polyline(wks,plot0(ip),xpts2,ypts,resl) 

;==============================

print("panel 8")
ip=5

; grids
  res@tmYMajorGrid                = True
  res@tmYMajorGridThicknessF      = 1.
  res@tmYMajorGridLineDashPattern = 2
  res@tmYMajorGridLineColor       = "grey40"

  res@tmYMinorGrid                = True
  res@tmYMinorGridThicknessF      = 0.5
  res@tmYMinorGridLineDashPattern = 2
  res@tmYMinorGridLineColor       = "grey50"

 data = data1D(7,:)

 res@trYMinF             = min(data)-0.05*abs(min(data))
 res@trYMaxF             = max(data)+0.05*abs(max(data))
 res@tiMainString        = " "
 res@tiYAxisString       = "LCL (m)"
 res@tiXAxisString       = "Hours UTC"

 res@xyLineColor = MyColors(3)  
 plot0(ip)  = gsn_csm_xy (wks,time,data,res)
 delete(data)

  poly1(ip) = gsn_add_polyline(wks,plot0(ip),xpts1,ypts,resl) 
  poly2(ip) = gsn_add_polyline(wks,plot0(ip),xpts2,ypts,resl) 


;============ PANEL ==================

  resP                    = True
  resP@gsnMaximize        = True
  resP@gsnPanelBottom     = 0.05
  resP@txString           = " "
  gsn_panel(wks,plot0,(/6,1/),resP)
 
 delete(plot0)
 delete(res)
 delete(resP)



end ; end of file
