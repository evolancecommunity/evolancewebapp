import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../App';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const LoadingSpinner = () => (
 <div className="flex justify-center items-center py-8">
    <Loader className="animate-spin h-8 w-8 text-purple-500" />
    <span className="ml-2 text-purple-500">Loading...</span>
 </div>
);

// Message Box for alerts

const MessageBox = ({ message, type, onClose,onConfirm }) => {
   const bgColor = type === 'error' ? 'bg-red-100 border-red-400 text-red-700' : 'bg-green-100 border-green-400 text-green-700';
   const borderColor = type === 'error' ? 'border-red-400' : 'border-green-400';
   const isConfirm = type === 'confirm';
   
   return (
     <div className={`fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50 p-4`}>
        <div className={`relative ${bgColor} border ${borderColor} px-4 py-3 rounded-lg shadow-lg max-w-sm w-full`}>
            <strong className='font-bold mr-2'>{isConfirm ? 'Confirm Action' : (type === 'error' ? 'Error!' : 'Success!')}</strong>
            <span className='block'>{message}</span>
            {isConfirm ? (
              <div className='mt-4 flex justify-end space-x-2'>
                <button onClick={()=>onClose(false)} className='px-4 py-2 bg-gray-300 text-gray-800 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition duration-150 ease-in-out'>
                  Cancel
                </button>
                <button onClick={()=>onConfirm(true)} className='px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition duration-150 ease-in-out'>
                  Confirm
                </button>
                </div>
               ):(
                <span className='absolute top-0 bottom-0 right-0 px-4 py-3'>
                  <button onClick={()=> onClose()} className='text-gray-500 hover:text-gray-700 focus:outline-none'>
                    <svg className='fill-current h-6 w-6' role='button' xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'>
                        <title>Close</title>
                      <path strokeLinecap='round' strokeLinejoin='round' strokeWidth={2} d='M6 18L18 6M6 6l12 12' />
                    </svg>
                  </button>
                </span>
                 
            )}
        </div>
     </div>
   );
};