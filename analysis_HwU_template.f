c
c This file contains the default histograms for fixed order runs: it
c only plots the total rate as an example. It can be used as a template
c to make distributions for other observables.
c
c This uses the HwU package and generates histograms in the HwU/GnuPlot
c format. This format is human-readable. After running, the histograms
c can be found in the Events/run_XX/ directory.
c
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      subroutine analysis_begin(nwgt,weights_info)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c This subroutine is called once at the start of each run. Here the
c histograms should be declared. 
c
c Declare the histograms using 'HwU_book'.
c     o) The first argument is an integer that labels the histogram. In
c     the analysis_end and analysis_fill subroutines this label is used
c     to keep track of the histogram. The label should be a number
c     starting at 1 and be increased for each plot.
c     o) The second argument is a string that will apear above the
c     histogram. Do not use brackets "(" or ")" inside this string.
c     o) The third, forth and fifth arguments are the number of bis, the
c     lower edge of the first bin and the upper edge of the last
c     bin.
c     o) When including scale and/or PDF uncertainties, declare a
c     histogram for each weight, and compute the uncertainties from the
c     final set of histograms
c
      implicit none
c In the weights_info, there is an text string that explains what each
c weight will mean. The size of this array of strings is equal to nwgt.
      character*(*) weights_info(*)
c Initialize the histogramming package (HwU). Pass the number of
c weights and the information on the weights:
      integer nwgt,i,l
      character*6 cc(2)
      data cc/'|T@SM',' '/
      call HwU_inithist(nwgt,weights_info)
c declare (i.e. book) the histograms
      do i=1,2
      l=(i-1)*4
      call HwU_book(l+1,'t pt             '//cc(i), 100,0.0d0,1000d0)
      call HwU_book(l+2,'tx pt            '//cc(i), 100,0.0d0,1000d0)
      call HwU_book(l+3,'h pt             '//cc(i), 100,0.0d0,1000d0)
      call HwU_book(l+4,'h inv_mass       '//cc(i), 100,0.0d0,500d0)
      enddo
      return
      end


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      subroutine analysis_end(dummy)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c This subroutine is called once at the end of the run. Here the
c histograms are written to disk. Note that this is done for each
c integration channel separately. There is an external script that will
c read the HwU data files in each of the integration channels and
c combines them by summing all the bins in a final single HwU data file
c to be put in the Events/run_XX directory, together with a gnuplot
c file to convert them to a postscript histogram file.
      implicit none
      double precision dummy
      call HwU_write_file
      return                
      end


cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
      subroutine analysis_fill(p,istatus,ipdg,wgts,ibody)
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c This subroutine is called for each n-body and (n+1)-body configuration
c that passes the generation cuts. Here the histrograms are filled.
      implicit none
c This includes the 'nexternal' parameter that labels the number of
c particles in the (n+1)-body process
      include 'nexternal.inc'
c This is an array which is '-1' for initial state and '1' for final
c state particles
      integer istatus(nexternal)
c This is an array with (simplified) PDG codes for the particles. Note
c that channels that are combined (i.e. they have the same matrix
c elements) are given only 1 set of PDG codes. This means, e.g., that
c when using a 5-flavour scheme calculation (massless b quark), no
c b-tagging can be applied.
      integer iPDG(nexternal)
c The array of the momenta and masses of the initial and final state
c particles in the lab frame. The format is "E, px, py, pz, mass", while
c the second dimension loops over the particles in the process. Note
c that these are the (n+1)-body particles; for the n-body there is one
c momenta equal to all zero's (this is not necessarily the last particle
c in the list). If one uses IR-safe obserables only, there should be no
c difficulty in using this.
      double precision p(0:4,nexternal)
c The weight of the current phase-space point is wgts(1). If scale
c and/or PDF uncertainties are included through reweighting, the rest of
c the array contains the list of weights in the same order as described
c by the weigths_info strings in analysis_begin
      double precision wgts(*)
c The ibody variable is:
c     ibody=1 : (n+1)-body contribution
c     ibody=2 : n-body contribution (excluding the Born)
c     ibody=3 : Born contribution
c The histograms need to be filled for all these contribution to get the
c physics NLO results. (Note that the adaptive phase-space integration
c is optimized using the sum of the contributions, therefore plotting
c them separately might lead to larger than expected statistical
c fluctuations).
      integer ibody, itop, ixtop, ihiggs
      integer i,l
c local variable
      double precision p_top(0:3),p_topx(0:3),p_higgs(0:3)
      double precision ptt,pttx,pth,mh
      double precision var,getpt,getinvm
      external getpt,getinvm
c
      itop=0
      ixtop=0
      ihiggs=0
      do i=1, nexternal
        if (ipdg(i).eq.6)then
                itop=i
        elseif (ipdg(i).eq.-6) then
                ixtop=i
        elseif (ipdg(i).eq.25) then
                ihiggs=i
        endif
      enddo
      do i=0,3
        if (itop.ne.0) p_top(i)=p(i,itop)
        if (ixtop.ne.0) p_topx(i)=p(i,ixtop)
        if (ihiggs.ne.0) p_higgs(i)=p(i,ihiggs)
      enddo
      ptt=getpt(p_top)
      pttx=getpt(p_topx)
      pth=getpt(p_higgs)
      mh=getinvm(p_higgs(0),p_higgs(1),p_higgs(2),p_higgs(3))
c Fill the histograms here using a call to the HwU_fill()
c subroutine. The first argument is the histogram label, the second is
c the numerical value of the variable to plot for the current
c phase-space point and the final argument is the weight of the current
c phase-space point.
      var=1d0
c always fill the total rate
      do i=1,2
      l=(i-1)*4
      call HwU_fill(l+1,ptt,wgts)
      call HwU_fill(l+2,pttx,wgts)
      call HwU_fill(l+3,pth,wgts)
      call HwU_fill(l+4,mh,wgts)
      enddo
      return
      end

      function getpt(p)
      implicit none
      real*8 getpt,p(0:3)
      getpt=dsqrt(p(1)**2+p(2)**2)
      return
      end

      function getinvm(en,ptx,pty,pl)
      implicit none
      real*8 getinvm,en,ptx,pty,pl,tiny,tmp
      parameter (tiny=1.d-5)
      tmp=en**2-ptx**2-pty**2-pl**2
      if(tmp.gt.0.d0)then
        tmp=sqrt(tmp)
      elseif(tmp.gt.-tiny)then
        tmp=0.d0
      else
        write(*,*)'Attempt to compute a negative mass'
        stop
      endif
      getinvm=tmp
      return
      end
