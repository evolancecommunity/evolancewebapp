import { useState } from "react";
import React, { useState, useEffect } from 'react';
import { PlusCircle,ArrowLeft} from 'lucide-react'; // Added Ticket icon
const InteractionList = ({interactions, customerName, onAddInteraction, onBackToCustomers}) => {
  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case 'positive':
        return 'bg-green-100 text-green-800';
      case 'negative':
        return 'bg-red-100 text-red-800';
      case 'neutral':
        return 'bg-yellow-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg max-w-4xl mx-auto mt-8">
      <div className="flex justify-between items-center mb-6">
        <div className="flex space-x-3">
        <h2 className="text-2xl font-bold mb-6 text-gray-800">Interactions for {customerName}</h2>
        <button
          onClick={onBackToCustomers}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-gray-600 hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
        >
          <ArrowLeft className="h-5 w-5 mr-2"/>
          Back to Customers
        </button>
      <button
        onClick={onAddInteraction}
        className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-gray-600 hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
      >
        <PlusCircle className="h-5 w-5 mr-2"/>
        Add Interaction
      </button>
      {interactions.length === 0 ? (
        <p className="text-gray-600">No interactions found for this customer.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Summary</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Sentiment</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {interactions.map((interaction) => (
                <tr key={interaction.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{interaction.type}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{interaction.date}</td>
                  <td className="px-6 py-4 text-sm text-gray-500 max-w-xs overflow-hidden text-ellipsis">{interaction.summary}</td>
                  <td>
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getSentimentColor(interaction.sentiment)}`}>
                      {interaction.sentiment} ({Math.round(interaction.sentiment_score * 100)}%)
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
      </div>
    </div>
  );
}

export default InteractionList;