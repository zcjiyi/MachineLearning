/** 
 @cond
 ############################################################################
 # LGPL License                                                             #
 #                                                                          #
 # This file is part of the Machine Learning Framework.                     #
 # Copyright (c) 2010-2012, Philipp Kraus, <philipp.kraus@flashpixx.de>     #
 # This program is free software: you can redistribute it and/or modify     #
 # it under the terms of the GNU Lesser General Public License as           #
 # published by the Free Software Foundation, either version 3 of the       #
 # License, or (at your option) any later version.                          #
 #                                                                          #
 # This program is distributed in the hope that it will be useful,          #
 # but WITHOUT ANY WARRANTY; without even the implied warranty of           #
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
 # GNU Lesser General Public License for more details.                      #
 #                                                                          #
 # You should have received a copy of the GNU Lesser General Public License #
 # along with this program. If not, see <http://www.gnu.org/licenses/>.     #
 ############################################################################
 @endcond
 **/


#ifndef __MACHINELEARNING_DIMENSIONREDUCE_SUPERVISED_REDUCE_HPP
#define __MACHINELEARNING_DIMENSIONREDUCE_SUPERVISED_REDUCE_HPP


#include <boost/static_assert.hpp>
#include <boost/numeric/ublas/matrix.hpp>

#ifdef MACHINELEARNING_MPI
#include <boost/mpi.hpp>
#endif

#include "../../errorhandling/exception.hpp"
#include "../../tools/tools.h"


namespace machinelearning { namespace dimensionreduce {
        
    /** namespace for all supervised reducing algorithms **/
    namespace supervised {
        
        #ifndef SWIG
        namespace ublas = boost::numeric::ublas;
        #endif
        
        
        /** abstract class for supervised dimension reducing classes **/      
        template<typename T, typename L> class reduce
        {
            #ifndef SWIG
            BOOST_STATIC_ASSERT( !boost::is_integral<T>::value );
            #endif
            
            
            public :
            
                /** maps data to target dimension **/
                virtual ublas::matrix<T> map( const ublas::matrix<T>&, const std::vector<L>& ) = 0; 
            
                /** returns the mapped dimension **/
                virtual std::size_t getDimension( void ) const = 0; 
            
        };
        
    }
        
} }
#endif
