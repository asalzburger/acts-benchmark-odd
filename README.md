# acts-benchmark-odd

Benchmark and regression test of ACTS using the OpenDataDetector.
At current it runs 
 * single muon generation
 * fast track simulation
 * truth track fitting
 * combinatorial Kalman filter

It only builds the ACTS source code if the commit hash of ACTS has changed,
otherwise it re-used a recompiled artifact.