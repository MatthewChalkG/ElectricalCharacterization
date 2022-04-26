<h1>Thin Film Growth and Characterization of DyTe2</h1>

This repository contains the supplementary information discussed in the thesis text. This includes:

<ol>
  <li>Scripts for automated temperature control and measurement</li>
  <li>Scripts for data processing and fitting</li>
  <li>CAD for the design of the vacuum transport stage</li>
  <li>CAD for the design of the four-point vacuum stage</li>
  <li>Design files for custom PCBs</li>
</ol>


<h3>Automated temperature control and measurement </h3>

Scripts interface with measurement instruments over GPIB, GPIB via USB, and RS-232. Users must therefore have functional pyserial and pyvisa installations. Similarly, users must have functioning NI-VISA libraries, which can be downloaded from the National Instruments [website](https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html#442805).

The raw scripts used for data logging in this work are given in `sortedelectricaldata/datalogging`. In general, the scripts expect the following equipment:

1) Keithley 2110 connected to the K-type thermocouple, connected to the host computer over USB
2) Keithley 2000 connected to the thermistor, connected to the host computer over RS-232
3) Siglent SPD3303X connected to the Peltier element, conencted to the host computer over USB
4) Arduino relay control box, connected to the computer over USB. This lies between the Peltier element and SIglent SPD3303X
5) SRS SR830, connected to the computer over RS-232, and wired as described in the thesis text depending on application
6) BK Precision BK5491, connected to the computer over USB


Temperature control is done independently of resistance and temperature logging. The PID implementation is given in pidtemp.py. The temperature sweep is defined in function `tempSweepHyst`, and is broken into four sections: sweep from room temperature to minimum temperature, sweep from minimum temperature to room temperature, swep from room temperature to maximum temperature, and sweep from maximum temperature to room temperature. Users interested in modifying sweep temperatures should modify this function. PID coefficients are then given in ap`approach_desired_exit`, which sweeps to a given temperature and exits.

The script `log2lockins_par124_notc.py` logs temperature as measured by the thermistor, the in-phase component of the PAR124A output through the BK5491, and in phase, quadrature, magnitude, and phase outputs from the SR830. These are then processed after the experiment.

Several other scripts were used to collect I-V measurements. AC two-point I-V measurements were taken with the SR830, and scanned over frequency and voltage. Instrument logging and control are both implemented in `SR830-2pt.py`.

Other utility scripts are also provided, such as `list\_pyvisa\_devices.py`, which lists the names of all pyvisa devices, which includes devices connected through GPIB over USB.

Note that the scripts do not automatically select the correct USB or serial port. Users will need to edit the script to match the port name with that of the instrument.


<h3> Data Processing </h3>

Raw data logged from the measurement scripts was processed and fitted using a series of Python scripts. These are given along with the raw data, in `sortedelectricaldata/dataprocessing`. Several scripts should run without arguments and produce plots and fits, including:

<ol>
  <li>`calcurve.py` </li>
  <li>`plotairdegradation.py` </li>
  <li>`plotallcontacts.py` </li>
  <li>`plotallcontacts_dc_vs_ac.py` </li>
  <li>`plotallcontacts_feb04.py` </li>
  <li>`plotivvsfreq.py` </li>
</ol>

The most complex script calculates the resistance-temperature curve and extrapolates a transport gap over time. This requires calibrating the PAR124A measurements, extracting the resistance and temperature timeseries, choosing regions of the timeseries corresponding to individual temperature loops, and fitting to extract the bandgap over time.

Much of this has been automated in the script `plotrt.py`, which provides several options in the `mode` variable:

<ol>
  <li>`choosepoints`: plots the raw resistance and temperature timeseries to allow the user to manually choose the index intervals corresponding to each temperature sweep. Also contains basic automated fitting functionality to identify each sweep region </li>
  <li>`testrt`: plots resistance against temperature for each sweep identified in `sweep_points`</li>
  <li>`fitrt`: fits each temperature-resistance sweep to the transport gap model, and provides summary statsitics</li>
  <li>`plotrt`: plots raw temperature and resistance timeseries in a pretty format</li>
  <li>`twopoint`: deprecated</li>
  <li>`plotdetvtime`: plots fitting parameters against time</li>
</ol>

<h3> CAD Design Files </h3>

CAD files for the glovebox and vacuum transport stage are both included in .zip files. These are both works in progress, so users considering assembling a similar stage are encouraged to contact Kaveh Pezeshki (kpezeshki@hmc.edu) for an up-to-date summary and design. Parts were designed in Solidworks 2020, but these files will be converted to other file formats on request.

<h3> PCB Design Files </h3>

PCB CAD files for the chip carrier, chip carrier receptacle, and the four-point stage are also available in .zip files. The PCBs were designed in KiCAD, and Gerbers will be provided on request.
